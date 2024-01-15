import json
import socket
import threading
from ast import literal_eval
import subprocess
import re
import psutil
import platform
import psycopg2
import datetime
import time


def get_cpu_info():
    cpu_info = psutil.cpu_percent()
    return cpu_info


def get_memory_info():
    memory_info = psutil.virtual_memory().percent

    return memory_info


def get_disk_info():
    disk_info = {}
    disk_info['c_precent'] = psutil.disk_usage("C:\\").percent
    disk_info['d_precent'] = psutil.disk_usage("D:\\").percent
    return disk_info


def get_ip():
    # 获取本机IP地
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(('8.8.8.8', 80))
    # ip = s.getsockname()[0]
    # s.close()
    ip_address = socket.gethostbyname(socket.gethostname())
    return ip_address


def get_net_io():
    net_io = {}
    # net_io['bytes_total'] = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
    net_io['packet_sent'] = psutil.net_io_counters().bytes_sent
    net_io['packet_recv'] = psutil.net_io_counters().bytes_recv
    # print(net_io)
    return net_io


def get_time():
    time = datetime.datetime.now()
    return time


def get_wifi():
    result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'])
    output = result.decode('gbk')

    # 初始化一个字典来存储WiFi信息
    wifi_info = {}

    # 使用正则表达式提取关键信息
    ssid_match = re.search(r"SSID\s*:\s*(.*)", output)
    if ssid_match:
        # print(ssid_match.group())
        wifi_info['SSID'] = ssid_match.group(1).strip()

    network_name_match = re.search(r"名称\s*:\s*(.*)", output)
    if network_name_match:
        # print(network_name_match)
        wifi_info['name'] = network_name_match.group(1).strip()
    return wifi_info

def get_battery():
    battery = psutil.sensors_battery().percent
    return battery

def insert_data():
    global i
    while True:
        # print(i)
        time.sleep(0.2)
        if i == 0:
            cursor.execute("truncate info")
        i = i + 1
        if (i >= 100):
            cursor.execute("DELETE FROM info WHERE time = (SELECT min(time) FROM info)")
            i = i - 1
        # 创建游标
        # cursor = conn.cursor()
        # 将数据插入数据库
        info['cpu_usage'] = get_cpu_info()  #######
        info['memory_usage'] = get_memory_info()  ######
        disk_info = get_disk_info()
        info['disk_c'] = disk_info['c_precent']  ####
        info['disk_d'] = disk_info['d_precent']  ####
        info['ip_addr'] = get_ip()  ####
        net_info = get_net_io()
        info['packet_sent'] = round(net_info['packet_sent'] / 3,2) ####
        info['packet_recv'] = round(net_info['packet_recv'] /3,2) ####
        info['time'] = get_time()  ####
        wifi_info = get_wifi()
        info['name'] = wifi_info['name']  ####
        info['ssid'] = wifi_info['SSID']  ####
        info['battery'] = get_battery()  ####

        cursor.execute(
            "INSERT INTO info (time,cpu_usage,memory_usage,disk_c,disk_d,ip_addr,packet_sent,packet_recv,name,ssid,battery) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (info['time'], info['cpu_usage'], info['memory_usage'], info['disk_c'], info['disk_d'], info['ip_addr'],
             info['packet_sent'], info['packet_recv'], info['name'], info['ssid'],info['battery'],))
        # 提交更改
        conn.commit()




def get_data():
    global cpu_usage, memory_usage, packet_sent, packet_recv
    try:
        while True:
            try:
                cursor.execute(
                    "SELECT (cpu_usage,memory_usage,packet_sent,packet_recv,disk_c,disk_d,ip_addr,name,ssid,battery) FROM info order by time desc limit 1")
                # 第一个是最新的
                # data = cursor.fetchall()
                # if data is None:
                #     print("data is none")
                break
            except Exception as e:
                # print(data1)
                print(f"error1：{e}")
                continue
        data1 = cursor.fetchall()
        json_data = {}
        for items in data1:
            for item in items:
                # print(item)
                item = item[1:-1].split(',')
                cpu_usage.insert(0, item[0])
                cpu_usage.pop()
                memory_usage.insert(0, item[1])
                memory_usage.pop()
                packet_sent.insert(0, item[2])
                packet_sent.pop()
                packet_recv.insert(0, item[3])
                packet_recv.pop()
                json_data['cpu_usage'] = cpu_usage
                json_data['memory_usage'] = memory_usage
                json_data['packet_sent'] = packet_sent
                json_data['packet_recv'] = packet_recv
                json_data['disk_c'] = item[4]
                json_data['disk_d'] = item[5]
                json_data['ip_addr'] = item[6]
                json_data['name'] = item[7]
                json_data['ssid'] = item[8]
                json_data['battery'] = item[9]

        return json.dumps(json_data)
    except Exception as e:
        print(f"error2：{e}")
        return json.dumps({"error":"222"})






if __name__ == "__main__":
    conn = psycopg2.connect(
        host="localhost",
        database="rasp",
        user="postgres",
        password="777777"
    )
    cursor = conn.cursor()
    i = 0
    info = {}
    cpu_usage = [0] * 16
    memory_usage = [0] * 16
    packet_sent = [0] * 16
    packet_recv = [0] * 16
    # 启动插入数据线程
    insert_data_thread = threading.Thread(target=insert_data)
    # 启动线程
    insert_data_thread.start()
    # while True:
    #     try:
    #         time.sleep(0.01)
    #         get_data()
    #     except Exception as e:
    #         print(f"error3:{e}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定地址和端口
    server_address = ('0.0.0.0', 8888)
    server_socket.bind(server_address)
    # 监听连接
    server_socket.listen()
    connection, addr = server_socket.accept()
    print("connected")
    while True:
        try:
            connection.recv(1024)
            data = get_data()
            connection.sendall(data.encode('utf-8'))
        except Exception as e:
            print(f"error2:{e}")

    # server_thread.start()

    # insert_data_thread.join()
    # server_thread.join()
