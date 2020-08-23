import os
import time
import boto3
from utils import statefile_to_dict
from botocore.errorfactory import ClientError


image_processing_bucket = "async-image-processing-demo"

def safe_create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


class BucketManager():

    def __init__(self, bucket_name, photos_path = "new_temp_photos"):
        self.s3 = boto3.client("s3")
        self.bucket_name = bucket_name
        self.bucket_images_folder = "images"
        self.bucket_results_folder = "results"
        self.photos_path = photos_path
        self.state_file_dict = statefile_to_dict(photos_path+"/state_file.txt")
    
    def send_data(self, local_file_path, remote_file_path):
        try:
            response = self.s3.upload_file(local_file_path,self.bucket_name,remote_file_path)
        except ClientError as e:
            logging.error(e)
            print("Error: ", e)
            
    def download_data(self, remote_file_path, local_file_path):
        try:
            response = self.s3.download_file(self.bucket_name,remote_file_path,local_file_path)
        except ClientError as e:
            print("Error: ", e)
            
            
    def verify_file_existence(self, remote_file_path):
        try:
            response = self.s3.head_object(Bucket = self.bucket_name, Key = remote_file_path)
            return True
        except ClientError as e:
            return False
        
    def verify_finish_processing(self):
        all_exists = True
        for filename, verification in self.state_file_dict.items():
            if verification != "OK":
                continue

            no_file_extension_name = filename.split(".")[0]
            file_extension = filename.split(".")[1]
            files_extension = [".json", "_bbx."+file_extension, "_rotate."+file_extension]
            for extension in files_extension:
                remote_file_path= self.bucket_results_folder+"/"+no_file_extension_name+extension
                
                print(remote_file_path)
                print(self.verify_file_existence(remote_file_path))
                all_exists = (all_exists and self.verify_file_existence(remote_file_path))
                
        return all_exists
    
    
    def wait_bucket_processing(self, sleep_time=10):
        print("processing images...")
        while True:
            time.sleep(10)
            if self.verify_finish_processing():
                print("images processed!")
                break
    
    
    def send_receive_images(self):
        for file in os.listdir(self.photos_path):
            if file == "state_file.txt":
                continue
                
            local_file_path = self.photos_path+"/"+file
            remote_file_path = self.bucket_images_folder+"/"+file
            self.send_data(local_file_path, remote_file_path)
    
        
    def get_bucket_results(self, results_folder = "temp_results"):
        print("downloading results...")
        safe_create_folder(results_folder)
        for filename, verification in self.state_file_dict.items():

                if verification != "OK":
                    continue

                no_file_extension_name = filename.split(".")[0]
                files_extension = [".json", "_bbx.JPG", "_rotate.JPG"]

                for extension in files_extension:
                    remote_file_path = self.bucket_results_folder+"/"+no_file_extension_name+extension
                    local_file_path = results_folder+"/"+no_file_extension_name+extension
                    self.download_data(remote_file_path, local_file_path)
        
        print("results downloaded!")
        
if __name__ == "__main__":
    bm = BucketManager(image_processing_bucket)
    print(bm.verify_finish_processing())
    
    