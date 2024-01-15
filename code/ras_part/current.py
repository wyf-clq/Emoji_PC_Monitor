import psutil
from PIL import Image, ImageDraw
import os
import sys 
import time
import logging
import spidev as SPI
from color_schemes import ColorScheme
from datetime import datetime
sys.path.append("..")
from lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz
import RPi.GPIO as GPIO
import threading

# def get_time_zones():
def 时间の旅人():
    global 时间表
    # 定义各地区的时区
    time_zones = {
        "America/New_York": "美国（纽约）时间",
        "Asia/Shanghai": "中国（上海）时间",
        "Europe/Brussels": "欧洲（布鲁塞尔）时间"
    }

    time_strings = {}
    while True:
    # 遍历时区，获取对应的时间
        for tz in time_zones:
            # 设置时区
            time_zone = pytz.timezone(tz)
            # 获取该时区的时间
            current_time = datetime.now(time_zone)
            # 格式化生成字符串
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            time_strings[tz] = formatted_time

        时间表 = time_strings
   
    

时间表 = {}

threading.Thread(target=时间の旅人).start()


def my_callback(channel):
    global counte
    counte += 1

counte = 1

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
Font2 = ImageFont.truetype("../Font/Font01.ttf", 44)
Font3 = ImageFont.truetype("../Font/Font02.ttf", 35)

# wait for update the ram_history
时区列表 = ["America/New_York", "Asia/Shanghai", "Europe/Brussels"]
# print(len(ram_history))
while True:

    
    # 时区 = "America/New_York"
    时区 = 时区列表[counte%3]
    print(时间表)
    image = Image.new("RGB", (disp.height, disp.width), "WHITE")
    draw = ImageDraw.Draw(image)
    # draw.rectangle([(0, 0), (280, 240)], fill = display_color)
    draw.rectangle([(0, 0), (280, 240)], fill = display_color)
    
    draw.line([(0, 240), (280, 240)], fill = background_color, width = 80)
    draw.text((80, 200), 'Current Time', fill = text_color, font=Font3)
    
    draw.text((25, 20), 时区, fill = "#36648B", font = ImageFont.truetype("../Font/Font02.ttf", 40))
    draw.text((53, 70), 时间表[时区].split(" ")[1], fill = background_color, font=ImageFont.truetype("../Font/Font02.ttf", 62))
    draw.text((95, 140), 时间表[时区].split(" ")[0], fill = "#00868B", font=ImageFont.truetype("../Font/Font02.ttf", 35))

    disp.ShowImage(image)