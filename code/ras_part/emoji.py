
#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet

# 表情展示和几个传感器的读入
import os
import shutil
import sys 
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
import threading 
import pickle

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
ImagePath = ""
disp = LCD_1inch69.LCD_1inch69()
disp.Init()
disp.clear()

Font1 = ImageFont.truetype("../Font/Font01.ttf", 25)
Font2 = ImageFont.truetype("../Font/Font01.ttf", 35)
Font3 = ImageFont.truetype("../Font/Font02.ttf", 32)

image1 = Image.new("RGB", (disp.width,disp.height ), "BLACK")
draw = ImageDraw.Draw(image1)
total = [0]*5
MPU_state = 0

def MPU_event_detect():
    global MPU_state,emoji_event
    while True:
        time.sleep(0.1)
        shutil.copyfile('./mpu_EVENT.pkl', './mpu_event_read.pkl')
        while True:
            try:
                with open('./mpu_event_read.pkl', 'rb') as file:
                    MPU_state = pickle.load(file)
                    break
            except Exception as e:
                continue
        print(MPU_state)
        if MPU_state > 650:
            emoji_event = True

threading.Thread(target = MPU_event_detect).start()

counter = 0
emoji_event = False
timer = [0,0]
# GPIO.setmode(GPIO.BCM)
# button_pin = 4
# GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.add_event_detect(button_pin, GPIO.RISING, callback=my_callback, bouncetime=300)



threshold = 1000
# async def DISPLAY():
while True:

    
    for i in range(0, 94):
        if emoji_event:
            break
        image = Image.open("./stand_by/stand_by"+f"{i:03d}"+".jpg")	
        disp.ShowImage(image)
        
    
    if emoji_event and MPU_state > threshold:
        for i in range(37):
            image = Image.open('./fear/fear'+f"{i:02d}"+".jpg")	
            disp.ShowImage(image)
        time.sleep(0.5)    
        emoji_event = False
    elif emoji_event and MPU_state < threshold:
        for i in range(40):
            image = Image.open('./happy/happy'+f"{i:02d}"+".jpg")	
            disp.ShowImage(image)
        time.sleep(0.5)    
        emoji_event = False
    else:
        pass


