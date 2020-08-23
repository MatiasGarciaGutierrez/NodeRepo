from UploadWatcher import UploadWatcher
from BucketManager import BucketManager
from utils import upload_json_files
from utils import change_folder_name

image_processing_bucket = "async-image-processing-demo"



if __name__ == "__main__":
    
    uw = UploadWatcher()
    
    while True:
    
        uw.wait_for_device_connection()
        uw.safe_download()

        bm = BucketManager(image_processing_bucket)

        bm.send_receive_images()
        bm.wait_bucket_processing()
        bm.get_bucket_results()

        upload_json_files()
        change_folder_name()
    
    
    