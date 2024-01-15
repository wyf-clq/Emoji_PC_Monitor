import socket
import json
import time
def client():
    host = '10.12.18.211'
    port = 8888

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("连接成功！")
    global cpu_usage,memory_usage,packet_recv,packet_sent,disk_C,disk_D,ip_addr,WLAN_NAME,SSID_NAME
    
    while True:
        try:
            msg = "give_give_give"
            client_socket.send(msg.encode())
            time.sleep(0.75)
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            json_data = json.loads(data)
            cpu_usage = json_data['cpu_usage']
            print(cpu_usage)


            with open('data.json', 'w') as f:
                json.dump(json_data, f)

            memory_usage = json_data['memory_usage']
            packet_sent = json_data['packet_sent']
            packet_recv = json_data['packet_recv']
            disk_C = json_data['disk_c']
            disk_D = json_data['disk_d']
            ip = json_data['ip_addr']
            WLAN_NAME = json_data['name']
            SSID_NAME = json_data['ssid']
        except Exception as e:
            print(e)

cpu_usage = [0]*16
memory_usage = [0]*16
packet_sent = [0]*16
packet_recv = [0]*16

disk_C = 0.5
disk_D = 0.5
ip_addr = '10.15.18.211'
WLAN_NAME = 'WLAN'
SSID_NAME = 'SUSTech-wifi'
# print("oooooooo")
if __name__ == '__main__':
    # print("ssss")
    client()    
    # print("kkkk")
