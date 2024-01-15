import psutil
from PIL import Image, ImageDraw
import os
import sys 
import time
import logging
import spidev as SPI
from color_schemes import ColorScheme
import client
sys.path.append("..")
from lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont
import copy 
import ast
import json 
import shutil

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

# wait for update the cpu_history
cpu_history = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# for i in range(16):
#     cpu_history[i] = psutil.cpu_percent()
# cpu_history = copy.deepcopy(cpu_usage)
# print(cpu_history)
last_cpu = []
while True:
    time.sleep(0.1)
    
    copied_data = None
# Verifying by loading data from 'copy.json'
    while True:
        try:
            with open('copy.json', 'r') as file:
                copied_data = json.load(file)
                cpu_historys = (copied_data['cpu_usage'])
                cpu_history = [float(item) for item in cpu_historys]
            break
        except Exception as e:
            print(e)
            continue

    

    # cpu_usage = psutil.cpu_percent()
    # cpu_history.insert(0,cpu_usage)
    # cpu_history.pop()
    
   
    ave = (sum(cpu_history)/len(cpu_history))
    mid = min((ave-ave%20)/20, 2)
    # print(cpu_history)

    # print(ave)
    # print(mid)
    scale = 200/(20+mid*40)
    x = 270
    image = Image.new("RGB", (disp.height, disp.width), "WHITE")
    draw = ImageDraw.Draw(image)
    # draw.rectangle([(0, 0), (280, 240)], fill = display_color)
    draw.rectangle([(0, 0), (280, 240)], fill = display_color)
    for i in cpu_history:
        draw.line([(x, 200-i*scale), (x, 200)], fill = pillar_color, width = 10)
        x -= 20
    draw.line([(0, 240), (280, 240)], fill = background_color, width = 80)
    draw.text((80, 200), 'CPU Usage', fill = text_color, font=Font3)
    draw.text((20, 50), f'{cpu_history[0]}%', fill = "#B03060", font=Font2)
    draw.text((20, 20), f'Range(0%, {20+mid*40}%)', fill = "#27408B", font=Font2)


    disp.ShowImage(image)

