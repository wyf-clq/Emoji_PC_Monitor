
#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
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
import time


def displayTime(timeString):
    image1 = Image.new("RGB", (disp.height,disp.width ), "WHITE")
    draw = ImageDraw.Draw(image1)
    # level = 14 + (high*1.05+margin)*(state%6)
    level = 18 + ((counte)%6)*high
    draw.rectangle([(0, 0), (2000, 2000)], fill = background_color, outline=None)

    draw.text((60,75), timeString, fill = text_color,font=ImageFont.truetype("../Font/Font02.ttf", 75))


    image1=image1.rotate(0)
    disp.ShowImage(image1)



def countdown(t):
    while t:
        if not start_timing:
            break
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        # print(timer, end="\r")  # Overwrite the previous line
        time.sleep(1)
        displayTime(timer)
        t -= 1



    print("Time's up!")

# Example usage
countdown_time = 60  # 60 seconds countdown

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

start_timing = False

def my_callback(channel):
    global counte,start_timing

    start_time = time.time()

    # 等待按钮释放
    while GPIO.input(button_pin) == GPIO.HIGH:
        time.sleep(0.01)

    duration = time.time() - start_time
    if duration > 1:  # 定义长按时间，这里是2秒
        print("长按检测到")
        start_timing = not start_timing
    else:
        counte += 1

        


counte = 1

GPIO.setmode(GPIO.BCM)

button_pin = 4
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=my_callback, bouncetime=300)
bus = smbus.SMBus(1) 
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


high = 35
init_y = 13
margin = 5
state = 0
hole_state = 0
while True:
    if start_timing:
        countdown((counte%6)*30)
        if start_timing:
            displayTime("00:00")
            time.sleep(3)
            start_timing = False
    
    image1 = Image.new("RGB", (disp.height,disp.width ), "WHITE")
    draw = ImageDraw.Draw(image1)
    # level = 14 + (high*1.05+margin)*(state%6)
    level = 18 + ((counte-1)%6)*high
    draw.rectangle([(0, 0), (2000, 2000)], fill = background_color, outline=None)

    draw.rectangle([(0, level), (2000, level+high+margin)], fill = rectangle_color, outline=None)
    # draw.line([(0, 0), (0, 240)], fill = rectangle_color, width = 95)

    draw.text((50,init_y), u" 30 s ", fill = text_color,font=Font3)
    draw.text((50,init_y+high+margin), u" 1 min", fill = text_color,font=Font3)
    draw.text((50,init_y+2*high+margin), u" 1 min 30 s ", fill = text_color,font=Font3)
    draw.text((50,init_y+3*high+margin), u" 2 min ", fill = text_color,font=Font3)
    draw.text((50,init_y+4*high+margin), u" 2 min 30 s ", fill = text_color,font=Font3)
    draw.text((50,init_y+5*high+margin), u" 3 min ", fill = text_color,font=Font3)

    # bx = 220
    # by = 180
    # batteray_level = by + 16
    # draw.rectangle([(bx, by), (bx + 20, by + 30)], fill = text_color, outline=None)
    # draw.rectangle([(bx+5, by-4), (bx + 15, by)], fill = text_color, outline=None)
    # draw.rectangle([(bx+4, by+4), (bx + 16, batteray_level)], fill = background_color, outline=None)

    image1=image1.rotate(0)
    disp.ShowImage(image1)

    

