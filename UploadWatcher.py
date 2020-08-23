import os
import time
from utils import statefile_to_dict
from utils import verify_files_state
from utils import count_receive_images
from utils import get_receive_images_list
from utils import write_dict_to_csv

gatweway_token = "PCqM4O9IqkH74lrIgiDH"

class UploadWatcher():
    
    def __init__(self, folder_name = "new_temp_photos"):
        self.folder_name = folder_name
        
    def wait_for_device_connection(self, wait_time = 5):
        print("waiting for device connection...")
        while True:
            if (os.path.exists(self.folder_name+"/state_file.txt")):
                print("device connected!")
                return True
            time.sleep(wait_time)
    
    def wait_for_download(self, time_out=60):
        last_receive_num = 0
        repeate_counter = 0
        
        while True:
            self.update_test_file()
            if (verify_files_state()):
                break
            receive_images = count_receive_images()
            if (receive_images == last_receive_num):
                repeate_counter += 1
            else:
                repeate_counter = 0
            time.sleep(15)
            
            
            print("received images: {} last received num {}".format(receive_images, last_receive_num))
            last_receive_num = receive_images
            if repeate_counter == 6:
                break
                
    def update_test_file(self):
        state_file = self.folder_name+"/state_file.txt"
        receive_images_list = get_receive_images_list(self.folder_name)
        state_file_dict = statefile_to_dict()
        
        for receive_image in receive_images_list:
            state_file_dict[receive_image] = "OK"
    
        write_dict_to_csv(state_file_dict, state_file)

    def safe_download(self, times = 3):
        for i in range(times):
            print("Intento {} de descarga".format(i+1))
            self.wait_for_download()
            self.update_test_file()
            if verify_files_state():
                print("Files download succefully!")
                break
            
            
            
if __name__ == "__main__":
    uw = UploadWatcher()
    
    uw.wait_for_device_connection()
    
    
    uw.safe_download()
    
    
    
                
      
                
        
       
                
                
                
            
            
            
            
            
    
        
        