import torch
from tqdm import tqdm
import time
from datetime import datetime
import os
from typing import Dict
import logging
from torchvision import models
import re
from base_train import BaseTrainer
from optimizer_function_factory import OptimizerFactory
from loss_function_factory import LossFunctionFactory

class InceptionNetv3Trainer(BaseTrainer) :
    def __init__(self, dataloader: Dict[str, torch.utils.data.DataLoader], options:dict, log: logging):
        
        self.train_options = options["train"]["InceptionNetv3"]["train_args"]
        
        self.save_dir = self.create_unique_directory(self.train_options['save_dir'])
        self.device = torch.device(self.train_options['cuda']) if torch.cuda.is_available() else torch.device('cpu')
        self.num_classes = self.train_options['num_classes']
        self.num_epochs = self.train_options['epochs']
        self.batch_size = self.train_options['batch_size']
        
        self.model = self.get_model(self.num_classes).to(self.device)
        
        self.criterion = LossFunctionFactory.get_loss_function(self.train_options['loss_function'])

        self.optimizer = OptimizerFactory.get_optimizer(
            self.train_options['optimizer'], self.model.parameters(), self.train_options['lr'], self.train_options['weight_decay']
        )
        
        self.lr_scheduler = self.get_lr_scheduler(self.optimizer, self.train_options['lr_scheduler'])
        self.dataloader_dict = dataloader
        self.log = log
        
        
    def start_train(self):
        _, save_directory = self.train_model()
        self.log.debug(f"Model saved at {save_directory}")
        return save_directory
    
    def get_lr_scheduler(self,
                         optimizer: torch.optim.Optimizer,
                         lr_scheduler_config: dict
        ) -> torch.optim.lr_scheduler.ReduceLROnPlateau :
        
        return torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode=lr_scheduler_config['mode'], 
            factor=lr_scheduler_config['factor'], 
            patience=lr_scheduler_config['patience'], 
            verbose=lr_scheduler_config['verbose']
        )
        
    def create_unique_directory(self, base_dir):
        os.makedirs(base_dir, exist_ok=True)
        # base_dir 이하의 디렉토리를 전부 가져온다
        dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        # base_dir 이하의 exp 폴더들을 가지고와서 폴더 이름의 맨 끝에 숫자가 있으면 해당 숫자를 리스트에 담는다
        indexes = [int(re.search(r'exp(\d+)$', d).group(1)) for d in dirs if re.search(r'exp(\d+)$', d)]
        
        # 만약 index가 비어있으면 exp1을 새로 만든다
        if not indexes:
            new_dir = os.path.join(base_dir, 'exp1')
            os.makedirs(new_dir)
            return new_dir
        # else:
        #     # index를 정렬하고 가장 큰 idx값을 갖는 폴더안에 saved_models라는 폴더가 없으면 그냥 현재디렉토리를 반환한다.
        #     index = max(indexes)
        #     dir_path = os.path.join(base_dir, f'exp{index}')
        #     if not os.path.exists(os.path.join(dir_path, 'saved_models')):
        #         return dir_path
        
        #     # 그렇지 않으면 가장 큰 idx값에 1을 더해 새로운 exp를 만든다.
        #     next_index = max(indexes) + 1
        #     new_dir = os.path.join(base_dir, f'exp{next_index}')
        #     os.makedirs(new_dir)

        # 그렇지 않으면 가장 큰 idx값에 1을 더해 새로운 exp를 만든다.
        next_index = max(indexes) + 1
        new_dir = os.path.join(base_dir, f'exp{next_index}')
        os.makedirs(new_dir)

        return new_dir
    

    def get_model(self, num_classes) :
        model = models.inception_v3(pretrained=True)
        for param in model.parameters():
            param.requires_grad = False
    
        fc_in_features = model.fc.in_features
        model.fc = torch.nn.Linear(fc_in_features, num_classes)
        
        children_list = list(model.children())
        split_point = int(2/3 * len(children_list))
        
        for i in range(split_point):
            for param in children_list[i].parameters():
                param.requires_grad = False
                
        for i in range(split_point, len(children_list)):
            for param in children_list[i].parameters():
                param.requires_grad = True
                
        return model
    
    
    def train_epoch(self):
        self.model.train()
        running_loss, running_corrects = 0.0, 0

        for inputs, labels, _ in tqdm(self.dataloader_dict['train']):
            inputs = inputs.to(self.device)
            labels = labels.to(self.device)

            self.optimizer.zero_grad()

            outputs, aux_outputs = self.model(inputs)
            _, preds = torch.max(outputs, 1)

            loss1, loss2 = self.criterion(outputs, labels), self.criterion(aux_outputs, labels)
            loss = loss1 + 0.3 * loss2

            loss.backward()
            self.optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        epoch_loss = running_loss / len(self.dataloader_dict['train'].dataset)
        epoch_acc = running_corrects.double() / len(self.dataloader_dict['train'].dataset)

        return epoch_loss, epoch_acc
    
    
    def validate_epoch(self):
        self.model.eval()
        running_loss, running_corrects = 0.0, 0

        for inputs, labels, image_paths in tqdm(self.dataloader_dict['valid']):
            inputs = inputs.to(self.device)
            labels = labels.to(self.device)

            with torch.no_grad():
                outputs = self.model(inputs)
                _, preds = torch.max(outputs, 1)

                loss = self.criterion(outputs, labels)

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            
        epoch_loss = running_loss / len(self.dataloader_dict['valid'].dataset)
        epoch_acc = running_corrects.double() / len(self.dataloader_dict['valid'].dataset)

        return epoch_loss, epoch_acc
    
    def train_model(self):
        since = time.time()
        best_acc = 0.0

        self.log.debug(
            f"{self.__class__.__name__} :: Training begins with following settings: Epochs - {self.num_epochs}, Batch Size - {self.batch_size}, Optimizer - {self.optimizer}"
        )

        for epoch in range(self.num_epochs):
            self.log.debug('-' * 15)
            self.log.debug(f'Epoch {epoch + 1}/{self.num_epochs}')

            # Training
            train_loss, train_acc = self.train_epoch()
            val_loss, val_acc = self.validate_epoch()

            # Learning rate scheduler
            self.lr_scheduler.step(val_loss)

            # Log
            self.log.debug(
                f"Epoch {epoch + 1}/{self.num_epochs}, Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}"
            )
            self.log.debug(
                f"Epoch {epoch + 1}/{self.num_epochs}, Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, Learning Rate - {self.optimizer.param_groups[0]['lr']}"
            )
            self.log.debug(f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f}")
            self.log.debug(f"Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}")


            # Save model at best acc
            if val_acc > best_acc:
                best_acc = val_acc
                current_date, current_time = datetime.now().strftime('%Y_%m_%d'), datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                directory = os.path.join(self.save_dir, current_date)
                os.makedirs(directory, exist_ok=True)
                save_model_name = f'{current_time}_val_acc_{val_acc:.4f}_val_loss_{val_loss:.4f}.pth'
                torch.save(self.model.state_dict(), os.path.join(directory, save_model_name))

        # Save model at final epoch
        current_date, current_time = datetime.now().strftime('%Y_%m_%d'), datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        directory = os.path.join(self.save_dir, current_date)
        save_model_name = f'{current_time}_final_epoch_val_acc_{val_acc:.4f}_val_loss_{val_loss:.4f}.pth'
        torch.save(self.model.state_dict(), os.path.join(directory, save_model_name))

        # Result at the end of training
        time_elapsed = time.time() - since
        print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
        print(f'Best val Acc: {best_acc:.4f}')
        self.log.debug(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
        self.log.debug(f'Best val Acc: {best_acc:.4f}')

        return self.model, directory
    
