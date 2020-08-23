from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
import json
import time
import os
from tb_gateway_mqtt import TBGatewayMqttClient

gatweway_token = "PCqM4O9IqkH74lrIgiDH"

class GatewayUploader():
    
    def __init__(self, token, host='mindcloud.mindlabs.cl', certificate_path = "certificado.pem", port = 8883):
        
        self.host = host
        self.port = port
        self.certificate_path = certificate_path
        
        self.gateway = TBGatewayMqttClient(host, token)
        self.gateway.connect(tls=True, ca_certs = certificate_path, port = port)
        
    def send_message(self, device_name, data):
        self.gateway.gw_connect_device(device_name)
        result = self.gateway.gw_send_telemetry(device_name, data)
        print(result)
        success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
        print(success)
        self.gateway.gw_disconnect_device(device_name)
        
        print("desconectando")
        
    def close_connection(self):
        self.gateway.disconnect()
        
        
def upload_json_files(folder = "temp_results"):
    gu = GatewayUploader(gatweway_token)
    
    count = 1
    for file in os.listdir(folder):
        if (file.split(".")[1] == "json"):
            json_file = open("results/"+file)
            json_data = json.load(json_file)
            json_file.close()
            telemetry = {"ts": int(round(time.time() * 1000)), "values":json_data['metadata']}
            print(telemetry)
            
            print("send to : Punto de control "+str(count))
            gu.send_message("Punto de control "+str(count), telemetry)
            count += 1
    gu.close_connection()
        
    

if __name__ == '__main__':
    upload_json_files("results")

