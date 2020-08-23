import os
import time
import boto3
import shutil
import json
from gateway_uploader import GatewayUploader
from botocore.errorfactory import ClientError

gatweway_token = "PCqM4O9IqkH74lrIgiDH"

def count_elements_in_folder(folder_name = "new_temp_photos"):
    return len(os.listdir(folder_name))
    
def statefile_to_dict(filename = "new_temp_photos/state_file.txt"):
    file = open(filename)
    
    file_dict = {}
    for line in file:
        name_state = line.split(";")
        if name_state[0] == "state_file.txt":
            continue
        file_dict[name_state[0]] = name_state[1].rstrip("\n")
    return file_dict

def get_receive_images_list(folder_name = "new_temp_photos"):
    folder_list = os.listdir(folder_name)
    folder_list.remove("state_file.txt")
   
    return folder_list

def write_dict_to_csv(file_dict, filename = "new_temp_photos/state_file.txt"):
    file = open(filename, 'w')
    
    for key, value in file_dict.items():
        file.write(key+";"+value+"\n")
    
    file.close()
    
def change_folder_name():
    if os.path.exists("temp_photos"):
        shutil.rmtree("temp_photos")
    
    if os.path.exists("results"):
        shutil.rmtree("results")
        
    os.rename("new_temp_photos", "temp_photos")
    os.rename("temp_results", "results")
    
def verify_files_state():
    '''
    Put a timeout 
    '''
    state_file_dict = statefile_to_dict()
    for value in state_file_dict.values():
        if value == "NOK":
            return False
    return True

def count_receive_images():
    state_file_dict = statefile_to_dict()
    ok_count = 0
    for image_name, value in state_file_dict.items():
        if value == "OK":
            ok_count += 1
    
    return ok_count
        

def safe_create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        
        
def upload_json_files(folder = "temp_results"):
    gu = GatewayUploader(gatweway_token)
    
    count = 1
    for file in os.listdir(folder):
        if (file.split(".")[1] == "json"):
            json_file = open("temp_results/"+file)
            json_data = json.load(json_file)
            json_file.close()
            telemetry = {"ts": int(round(time.time() * 1000)), "values":format_msg(json_data)}
            print(telemetry)
            
            print("send to : Punto de control "+str(count))
            gu.send_message("Punto de control "+str(count), telemetry)
            count += 1
    gu.close_connection()
    

def format_msg(json_data):
    latitud = json_data['metadata']['Latitude']
    longitud = json_data['metadata']['Longitude']
    n_plantas = json_data['procesamiento']['cantidad_de_plantas']
    pixeles_maleza = json_data['procesamiento']['pixeles_maleza']
    pixeles_imagen = json_data['procesamiento']['pixeles_imagen_original']
    
    msg_dict = {'PlantQ':n_plantas, 
                'CropWeedPercentage':pixeles_maleza/pixeles_imagen, 
                'Latitude': latitud,
                'Longitude':longitud,
                'coordinates': '[[-36.833054, -72.115919],[-36.833751, -72.113068],[-36.834971, -72.115919]]'
               }
    
    return msg_dict
    
    
if __name__ == "__main__":
    file = "DJI_0001.json"
    json_file = open("results/"+file)
    json_data = json.load(json_file)
    json_file.close()
    
    latitud = json_data['metadata']['Latitude']
    longitud = json_data['metadata']['Longitude']
    n_plantas = json_data['procesamiento']['cantidad_de_plantas']
    pixeles_maleza = json_data['procesamiento']['pixeles_maleza']
    pixeles_imagen = json_data['procesamiento']['pixeles_imagen_original']
    
    msg_dict = {'PlantQ':n_plantas, 
                'CropWeedPercentage':pixeles_maleza/pixeles_imagen, 
                'Latitude': latitud,
                'Longitude':longitud,
                'coordinates': [[-36.833054, -72.115919],[-36.833751, -72.113068],[-36.834971, -72.115919]]
               }

    
    
    print(msg_dict)
    
    
    