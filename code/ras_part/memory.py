import psutil
from PIL import Image, ImageDraw
import os
import sys 
import time
import logging
import spidev as SPI
from color_schemes import ColorScheme
import client
import copy
import RPi.GPIO as GPIO
sys.path.append("..")
from lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont
import json


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

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level = logging.DEBUG)

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
    # display with hardware SPI:
# ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
#disp = LCD_1inch69.LCD_1inch69(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
disp = LCD_1inch69.LCD_1inch69()
# Initialize library.
disp.Init()
# Clear display.
disp.clear()

Font1 = ImageFont.truetype("../Font/Font00.ttf", 35)
Font2 = ImageFont.truetype("../Font/Font02.ttf", 28)
Font3 = ImageFont.truetype("../Font/Font02.ttf", 35)

# wait for update the ram_history
# ram_history = [0]*16
# for i in range(16):
#     ram_history[i] = psutil.virtual_memory().percent

# print(len(ram_history))
ram_history = [1]
disk_C = 0
disk_D = 0
while True:
    time.sleep(0.1)
    while True:
        try:
            with open('copy.json', 'r') as file:
                copied_data = json.load(file)
                ram_history = (copied_data['memory_usage'])
                ram_history = [float(item) for item in ram_history]
                # disk_C = copied_data['disk_c']
                disk_C = float(copied_data['disk_c'])
                disk_D = float(copied_data['disk_d'])
            break
        except Exception as e:
            print(e)
            continue
    
    if counte%2 == 0:
        ave = (sum(ram_history)/len(ram_history))
        mid = min((ave-ave%20)/20, 2)

        scale = 150/(20+mid*40)
        x = 270
        image = Image.new("RGB", (disp.height, disp.width), "WHITE")
        draw = ImageDraw.Draw(image)

        draw.rectangle([(0, 0), (280, 240)], fill = display_color)
        for i in ram_history:
            draw.line([(x, 200-i*scale), (x, 200)], fill = pillar_color, width = 10)
            x -= 20
        draw.line([(0, 240), (280, 240)], fill = background_color, width = 80)
        draw.text((80, 200), 'RAM Usage', fill = text_color, font=Font3)
        draw.text((20, 50), f'{ram_history[0]}%', fill = "#B03060", font=Font2)
        draw.text((20, 20), f'Range(0%, {20+mid*40}%)', fill = "#27408B", font=Font2)

        disp.ShowImage(image)
    else:
        image = Image.new("RGB", (disp.height, disp.width), "WHITE")
        draw = ImageDraw.Draw(image)

        draw.rectangle([(0, 0), (280, 240)], fill = display_color)
        draw.line([(0, 240), (280, 240)], fill = background_color, width = 80)
        draw.text((20, 20), f'Range(0%, 100%)', fill = "#27408B", font=Font2)
        # draw.text((20, 50), f'DISK C: {ram_history[-1]}%', fill = "#27408B", font=Font2)
        draw.rectangle([(60, 90), (100, 200)], fill = background_color)
        draw.rectangle([(160, 90), (200, 200)], fill = background_color)

        draw.rectangle([(60, 90), (100, 90+110 * ( 1 - 0.01 * disk_C ))], fill = '#00C5CD')
        draw.rectangle([(160, 90), (200, 90+110 * ( 1 - 0.01 * disk_D ))], fill = '#00C5CD')
       
        draw.text((20, 50), f'C: {disk_C}%,   D: {disk_D}%', fill = "#27408B", font=Font2)

        draw.text((65, 200), 'DISK Usage', fill = text_color, font=Font3)

        disp.ShowImage(image)