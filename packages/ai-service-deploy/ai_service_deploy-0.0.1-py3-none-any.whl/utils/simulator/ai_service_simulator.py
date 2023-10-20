from logging import Logger
import pandas as pd
import uuid
import io
from PIL import Image
import os
import numpy as np
from utils.fileparser import FileParserFactory
import threading
import lib.himsai_pb2 as himsai
import lib.himsai_pb2_grpc as himsai_grpc
import time
import grpc
from queue import Queue

class AiServiceSimulator() :
    def __init__(self, log: Logger) :
        self.logger = log
        self.ai_service = None

    async def _sim_send_to_client(self, image_id, label, score, result, client_address) :
        self.logger.debug(f"Simulator sent to client - {client_address}")
        return

    async def _sim_send_to_management(self, image_id, label, score, result, client_address) :
        self.logger.debug(f"Simulator sent to managment")
        return

    async def _sim_send_to_storage(self, image_id, byte_img) :
        self.logger.debug(f"Simulator sent to storage")
        return

    def _sim_model_processing_thread(self, material, profile_id, profile_name, inspection_model_info):
        self.logger.debug("model processing thread")
        return
    
    
    def _sim_create_by_client(self, ai_servicer) :
        """
        "./etc/options_material.json" 이 경로에서 마치 management가 보내준것 처럼 임의로 사용된다.
        
        """
        import uuid
        self.ai_service = ai_servicer
        
        parser_factory = FileParserFactory()
        
        parser = parser_factory.create_parser(self.ai_service.sim_get_client_options_path)
        option_config = parser.parse(self.ai_service.sim_get_client_options_path)
        
        parser = parser_factory.create_parser(option_config['D1'])
        option_d1 = parser.parse(option_config['D1'])
        
        parser = parser_factory.create_parser(option_config['D2'])
        option_d2 = parser.parse(option_config['D2'])
        
        parser = parser_factory.create_parser(option_config['D3'])
        option_d3 = parser.parse(option_config['D3'])
        
        parser = parser_factory.create_parser(option_config['D4'])
        option_d4 = parser.parse(option_config['D4'])


        while True :
            csv = pd.read_csv(self.ai_service.sim_get_client_data_path)
            img_files = csv["image"].to_list()

            for i, img_file in enumerate(img_files, start=1) :
                with open(img_file, 'rb') as f :
                    data = f.read()
                    
                image_id = str(uuid.uuid1().hex.upper())
                options = ""
                pp_config = '{"pre_process":{},"post_process":{}}'
                manager_address = f"{self.ai_service.sim_send_management_ip}:{self.ai_service.sim_send_management_port}"
                client_address = f"{self.ai_service.sim_get_client_ip}:{self.ai_service.sim_get_client_port}"
                image_data = io.BytesIO(data)
                np_request_image = np.array(Image.open(image_data).convert("L"))
                
                image_name, _ = os.path.splitext(img_file)
                material = image_name[-2:]

                if material == "D1" :
                    options = option_d1
                elif material == "D2" :
                    options = option_d2
                elif material == "D3" :
                    options = option_d3
                elif material == "D4" :
                    options = option_d4
                else :
                    options = option_d1
                
                option_dic = options
                #print(option_dic)
                
                profile_name, profile_id = option_dic['profile'], option_dic['profile_id']
                material, inspection_model_info  = option_dic['step'], option_dic['model']
                
                if material not in self.ai_service.model_list and material not in self.ai_service.model_loading_events:
                    self.ai_service.model_loading_events[material] = threading.Event()
                    threading.Thread(target=self.ai_service.model_download_function , args=(material, profile_id, profile_name, inspection_model_info)).start()
            
                 # Set manager address if none
                if self.ai_service.management_stub is None :
                    self.ai_service.management_channel = grpc.insecure_channel(f"{self.ai_service.sim_send_management_ip}:{self.ai_service.sim_send_management_port}")
                    self.ai_service.management_stub = himsai_grpc.ManagementStub(self.ai_service.management_channel)

                        
                # Put the request in the que
                self.ai_service.request_que.put((image_id, options, pp_config, manager_address, \
                    client_address, np_request_image, data, material))
                
                self.ai_service.ai_service.debug(f"Simulator Get data from client - {client_address}")
                            
                # Add a stub object for each client
                if client_address not in self.ai_service.client_stubs_dictionary:
                    client_channel = grpc.insecure_channel(client_address)
                    client_stub = himsai_grpc.ClientStub(client_channel)
                    self.ai_service.client_stubs_dictionary[client_address] = (client_stub, client_channel)

                time.sleep(1)