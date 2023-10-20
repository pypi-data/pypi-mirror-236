import torch
import torch.nn as nn
from torchvision.models import inception_v3
import torchvision.transforms as transforms
from PIL import Image
import io
from typing import List
import time
from collections import defaultdict
import numpy as np
from typing import Dict
import traceback


class ModelSim:
    def __init__(self) :
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.class_idx = {"0": "softdot_1", "1": "softline_2", "2": "darkline_4", "3": "darkspot_5", "4": "curvedline_6", "5": "black_7", "6": "normal_9"}

        self.model_path = None
        #'../src/models/exp53/saved_models/2023_08_10/2023_08_10_01_19_57_final_epoch_val_acc_0.9739_val_loss_0.0928.pth'
        self.num_classes = len(self.class_idx)
        self.model = None
        self.model_pred_dic = defaultdict(float)

    
    def PreLoadModels(self, model_path) :
        self.model_path = model_path


    def ImportModules(self, specID, specDic):
        model = inception_v3(pretrained=True)

        for param in model.parameters():
            param.requires_grad = False

        fc_in_features = model.fc.in_features
        model.fc = nn.Linear(fc_in_features, self.num_classes)

        children_list = list(model.children())
        split_point = int(2/3 * len(children_list))

        for i in range(split_point):
            for param in children_list[i].parameters():
                param.requires_grad = False

        for i in range(split_point, len(children_list)):
            for param in children_list[i].parameters():
                param.requires_grad = True

        model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        model = model.to(self.device)
        model.eval()

        self.model = model

        return []
    
    def modelLoaded(self) :
        return self.model

    def transform_byte_image(self, image_bytes):

        mean_list = [0.46679285168647766, 0.46679285168647766, 0.46679285168647766]
        std_list = [0.2517392933368683, 0.2517392933368683, 0.2517392933368683]

        
        transf = transforms.Compose([
            transforms.Resize((299, 299)),
            transforms.ToTensor(),
            transforms.Normalize(mean_list, std_list)
        ])


        try:
            start_time = time.time()
            image = Image.open(io.BytesIO(image_bytes))
            byte_to_image_time = time.time() - start_time

            start_time = time.time()
            transf_img = transf(image).to(self.device)
            transf_time = time.time() - start_time
            
            return transf_img
        except Image.UnidentifiedImageError:
            print("Error: Unable to identify the provided image.")
            return None
        
    def transform_numpy_image(self, image_np):

        mean_list = [0.46679285168647766, 0.46679285168647766, 0.46679285168647766]
        std_list = [0.2517392933368683, 0.2517392933368683, 0.2517392933368683]

        transf = transforms.Compose([
            transforms.Lambda(lambda x: x.convert("RGB")),
            transforms.Resize((299, 299)),
            transforms.ToTensor(),
            transforms.Normalize(mean_list, std_list)
        ])

        try:
            # convert numpy to PIL
            image = Image.fromarray(image_np)
            transf_img = transf(image).to(self.device)
            return transf_img
        except Exception as e:
            print(f"Error: Unable to process the provided image. Reason: {e}")
            traceback.print_exc()  # 에러의 traceback 정보를 출력
            return None
        
    def run(self, packs: List[Dict[str, List[np.ndarray]]], material):
        pack = packs[0]  # 첫 번째 요소만 추출
        batch_images = pack["data"]
        
        #tensor_list = [self.transform_numpy_image(img) for img in batch_images if self.transform_numpy_image(img) is not None]

        tensor_list = []
        for img in batch_images :
            processed_img = self.transform_numpy_image(img)
            if processed_img is not None :
                tensor_list.append(processed_img)


        if not tensor_list:
            print("Error: All provided images couldn't be processed")
            return []

        tensor_batch = torch.stack(tensor_list, dim=0)
        outputs = self.model.forward(tensor_batch)

        _, y_hats = outputs.max(1)
        probs = torch.nn.functional.softmax(outputs, dim=1)

        results = []
        for i in range(tensor_batch.size(0)):
            predicted_idx = str(y_hats[i].item())
            predicted_prob = round(probs[i][y_hats[i]].item(), 3)

            results.append({
                'result': self.class_idx[predicted_idx],  # Class name/index
                'score': predicted_prob,                  # Probability score
                'label': material                         # Material type
            })

        return results

    def run_byte(self, batch_images: List[bytes]):
        tensor_list = [self.transform_image(img) for img in batch_images if self.transform_byte_image(img) is not None]

        tensor_batch = torch.stack(tensor_list, dim=0)

        outputs = self.model.forward(tensor_batch)

        _, y_hats = outputs.max(1)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        results = []
        for i in range(tensor_batch.size(0)):

            predicted_idx = str(y_hats[i].item())
            predicted_prob = round(probs[i][y_hats[i]].item(), 3)
            results.append((self.class_idx[predicted_idx], predicted_prob))

        return results
    

    def non_preprocess_model_predict(self, tensor_img: List[bytes]):
        # A구간
        #tensor_list = [self.transform_image(img) for img in batch_images if self.transform_image(img) is not None]
        # A구간부터 여기까지는 0.003초에 가까움
        #self.model_pred_log.info(f"Function run time: {time.time() - start_t:.3f} seconds")
        tensor_img = self.bytes_to_tensor(tensor_img)
        tensor_batch = torch.stack(tensor_img, dim=0)

        # B구간
        outputs = self.model.forward(tensor_batch)
        _, y_hats = outputs.max(1)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        #self.model_pred_log.info(f"Function run time: {time.time() - start_t:.3f} seconds")
        # B구간부터 여기까지는 0.5~0.6초 정도

        # K구간
        results = []
        for i in range(tensor_batch.size(0)):
            predicted_idx = str(y_hats[i].item())
            predicted_prob = probs[i][y_hats[i]].item()
            results.append((self.class_idx[predicted_idx], predicted_prob))
        # K구간부터 여기 까지는 소요시간 0초에 가까움
        return results
    

    def dummy_model_predict(self, batch_images) :
        #tensor_list = [transform_image(img) for img in batch_images if transform_image(img) is not None]
        #tensor_batch = torch.stack(tensor_list, dim=0)

        num_images = len(batch_images)
        dummy_result = ('dummy', 0.9517058730125427)
        results = [dummy_result for _ in range(num_images)]    

        return results


