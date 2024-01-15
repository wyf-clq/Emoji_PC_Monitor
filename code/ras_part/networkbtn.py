
#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet

# 表情展示和几个传感器的读入
import os
import psutil
import sys 
from color_schemes import ColorScheme
import RPi.GPIO as GPIO
import smbus
import math
import time
import asyncio
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont
import client
import copy
import threading 
import json

IP = ""
name = ""
ssid = ""
sent_pack = []
recv_pack = []

def IP_info():
    global IP,name,ssid,sent_pack,recv_pack
    while True:
        while True:
            try:
                with open('copy.json', 'r') as file:
                    copied_data = json.load(file)
                
                    IP = copied_data['ip_addr']
                    name = copied_data['name']
                    ssid = copied_data['ssid']

                    sent_pack = [float(item)*0.000001 for item in copied_data['packet_sent']]
                    recv_pack = [float(item)*0.000001 for item in copied_data['packet_recv']]
                    # print("+++++++++++++++++++++++++")
                break
            except Exception as e:
                print(e)
                continue

threading.Thread(target=IP_info).start()
# Configuration initialization:
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level = logging.DEBUG)
logging.info("show image")
ImagePath = "./ZHJ_angry/anger"
disp = LCD_1inch69.LCD_1inch69()
disp.Init()
disp.clear()

Font1 = ImageFont.truetype("../Font/Font01.ttf", 25)
Font2 = ImageFont.truetype("../Font/Font01.ttf", 35)
Font3 = ImageFont.truetype("../Font/Font02.ttf", 32)

image1 = Image.new("RGB", (disp.height,disp.width), "BLACK")
draw = ImageDraw.Draw(image1)



# intialize MPU sensor

def my_callback(channel):
    global counte
    counte += 1

counte = 0

timer = [0,0]
GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()
button_pin = 4
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=my_callback, bouncetime=300)
bus = smbus.SMBus(1) 
address = 0x68       
bus.write_byte_data(address, power_mgmt_1, 0)
modern_scheme = ColorScheme.MODERN
# modern_scheme = ColorScheme.ELEGANT
# modern_scheme = ColorScheme.VIBRANT
# modern_scheme = ColorScheme.TECH
# modern_scheme = ColorScheme.NATURAL
text_color = modern_scheme.value['main']
background_color = modern_scheme.value['secondary']
rectangle_color = modern_scheme.value['accent']
display_color = modern_scheme.value['display']
pillar_color = modern_scheme.value['pillar']


sacle_list = [0,0]
sent_history = copy.deepcopy(client.packet_sent)
recv_history = copy.deepcopy(client.packet_recv)




while True:

    

    if counte%3 == 0:
        image = Image.new("RGB", (disp.height, disp.width), "WHITE")
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), (280, 240)], fill = display_color)
        draw.line([(0, 240), (280, 240)], fill = background_color, width = 80)
        draw.text((110, 200), 'IP info', fill = text_color, font=Font3)
        draw.text((20, 20), name, fill = background_color, font=ImageFont.truetype("../Font/Font02.ttf", 45))
        draw.text((20, 80), ssid, fill = "#00868B", font=ImageFont.truetype("../Font/Font02.ttf", 40))
        draw.text((20, 120), IP, fill = "#36648B", font = ImageFont.truetype("../Font/Font02.ttf", 40))

        disp.ShowImage(image)

    elif counte%3 == 1:
        scale = 0
        up_limit = 0
        ave_sent = sum(sent_pack)/len(sent_pack)
        # ave_recv = sum(recv_pack)/len(recv_pack)*0.000001
        if ave_sent < 10:
            up_limit = 10
        elif ave_sent < 20:
            up_limit = 20
        else:
            up_limit = 40

        scale = 150 / up_limit


        x = 270
        image = Image.new("RGB", (disp.height, disp.width), "WHITE")
        draw = ImageDraw.Draw(image)
        # draw.rectangle([(0, 0), (280, 240)], fill = display_color)
        draw.rectangle([(0, 0), (280, 240)], fill = display_color)
        for i in sent_pack:
            draw.line([(x, 200-i*scale), (x, 200)], fill = pillar_color, width = 10)
            x -= 20
        draw.line([(0, 240), (280, 240)], fill = background_color, width = 80)
        draw.text((80, 200), 'Sent Bytes', fill = text_color, font=Font3)
        draw.text((10, 20), 'Packet Sent', fill = "#27408B", font=Font3)
        draw.text((10, 53), f'{sent_pack[-1]:.2f}', fill = "#B03060", font=ImageFont.truetype("../Font/Font02.ttf", 40))
        draw.text((109, 60), f'MBps', fill = "#00008B", font=Font3)

        # draw.text((20, 20), f'Range(0%, {20+mid*40}%)', fill = "#27408B", font=Font2)


        disp.ShowImage(image)
    else:
        scale = 0
        up_limit = 0
        ave_recv = sum(recv_pack)/len(recv_pack)
        # ave_recv = sum(recv_pack)/len(recv_pack)*0.000001
        if ave_recv < 100:
            up_limit = 100
        elif ave_recv < 200:
            up_limit = 200
        else:
            up_limit = 400

        scale = 150 / up_limit


        x = 270
        image = Image.new("RGB", (disp.height, disp.width), "WHITE")
        draw = ImageDraw.Draw(image)
        # draw.rectangle([(0, 0), (280, 240)], fill = display_color)
        draw.rectangle([(0, 0), (280, 240)], fill = display_color)
        for i in recv_pack:
            draw.line([(x, 200-i*scale), (x, 200)], fill = pillar_color, width = 10)
            x -= 20
        draw.line([(0, 240), (280, 240)], fill = background_color, width = 80)
        draw.text((80, 200), 'Recv Bytes', fill = text_color, font=Font3)
        draw.text((10, 20), 'Packet Recv', fill = "#27408B", font=Font3)
        draw.text((10, 53), f'{recv_pack[-1]:.2f}', fill = "#B03060", font=ImageFont.truetype("../Font/Font02.ttf", 40))
        draw.text((140, 60), f'MBps', fill = "#00008B", font=Font3)

        # draw.text((20, 20), f'Range(0%, {20+mid*40}%)', fill = "#27408B", font=Font2)


        disp.ShowImage(image)




 
    

        


