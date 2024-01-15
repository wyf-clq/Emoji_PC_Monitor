import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from scipy.signal import TransferFunction, step
import os
from color_schemes import ColorScheme
import sys 
import time
import math
import logging
import client 
import subprocess
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont
import shutil
import json

def my_callback_click(channel):
    print(f"*************{channel}********")
    global counter,current_process,hole_state
    # 根据 counter 的值异步运行不同的 Python 文件
    if current_process == None:
        hole_state = counter
        if counter%6 == 5:
            current_process = subprocess.Popen(["python", "./emoji.py"])  #三种表情切换
        elif counter%6 == 0:
            current_process = subprocess.Popen(["python", "./cpu_usage.py"])
        elif counter%6 == 1:
            current_process = subprocess.Popen(["python", "./memory.py"]) 
        elif counter%6 == 3:
            current_process = subprocess.Popen(["python", "./networkbtn.py"])  #IP info and  sent/recv 可视化
        elif counter%6 == 2:
            current_process = subprocess.Popen(["python", "./current.py"])  #中国 美国 欧洲时间
        elif counter%6 == 4:
            current_process = subprocess.Popen(["python", "./Timer.py"]) 
    elif current_process!= None and current_process.poll() == None:
        current_process.terminate()
        current_process = None
        counter = hole_state
        print("Current process terminated.")



def my_callback(channel):
    print(f"+++++++++++++{channel}+++++++++++")

    global counter
    counter += 1
    # print(f"++++++++++{counter}+++++++++++")

counter = 0
current_process = None
timer = [0,0]
GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()
button_pin = 4
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=my_callback, bouncetime=300)

button_pin_click = 22
GPIO.setup(button_pin_click, GPIO.IN)
GPIO.add_event_detect(button_pin_click, GPIO.RISING, callback=my_callback_click, bouncetime=300)




# 定义主题色
modern_scheme = ColorScheme.MODERN
# modern_scheme = ColorScheme.ELEGANT
# modern_scheme = ColorScheme.VIBRANT
# modern_scheme = ColorScheme.TECH
# modern_scheme = ColorScheme.NATURAL


# 定义系统参数
omega_n = 10  # 自然频率
zeta = 1.0   # 阻尼比，小于1表示欠阻尼

# 创建传递函数
numerator = [omega_n**2]
denominator = [1, 2*zeta*omega_n, omega_n**2]
王逸凡の大作 = TransferFunction(numerator, denominator)

# 计算阶跃响应
t, y = step(王逸凡の大作)

# 绘制阶跃响应
# for time,v in zip(t,y):
#     print(f"time is {time:.2f}, y is {v:.2f}")

RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level = logging.DEBUG)


# display with hardware SPI:
''' Warning!!!Don't  creation of multiple displayer objects!!! '''
disp = LCD_1inch69.LCD_1inch69(spi=SPI.SpiDev(bus, device),spi_freq=40000000,rst=RST,dc=DC,bl=BL)
# disp = LCD_1inch69.LCD_1inch69()
# Initialize library.
disp.Init()
# Clear display.
disp.clear()

Font1 = ImageFont.truetype("../Font/Font01.ttf", 25)
Font2 = ImageFont.truetype("../Font/Font01.ttf", 35)
Font3 = ImageFont.truetype("../Font/Font02.ttf", 35)

# Create blank image for drawing.
text_color = modern_scheme.value['main']
background_color = modern_scheme.value['secondary']
rectangle_color = modern_scheme.value['accent']

high = 35
init_y = 13
margin = 5
state = 0
hole_state = 0
while True:
    shutil.copy('data.json', 'copy.json')


    while True:
        try:
            with open('copy.json', 'r') as file:
                copied_data = json.load(file)
                batteray = float(copied_data['battery'])
            break
        except Exception as e:
            print("first place")
            continue

    # print(client.message)
    bx = 220
    by = 180
    if current_process != None:
        time.sleep(0.2)
        continue
    if counter>state:
        print("animation")
        for i in range(0, len(y), 10):  # 从0开始，到列表长度，每10步取一次
            slice = y[i]  # 取从i开始的10个元素
            image1 = Image.new("RGB", (disp.height,disp.width ), "WHITE")
            draw = ImageDraw.Draw(image1)
            level = 18 + (state%6)*high+slice*(high)
            # print(level)
            draw.rectangle([(0, 0), (2000, 2000)], fill = background_color, outline=None)
            # draw.line([(0, 0), (0, 240)], fill = rectangle_color, width = 95)

            draw.rectangle([(0, level), (2000, level+high+margin)], fill = rectangle_color, outline=None)
            draw.text((15,init_y), u"1. CPU Usage", fill = text_color,font=Font3)
            draw.text((15,init_y+high+margin), u"2. Memory Utilization", fill = text_color,font=Font3)
            draw.text((15,init_y+2*high+margin), u"3. Current Time", fill = text_color,font=Font3)
            draw.text((15,init_y+3*high+margin), u"4. Network", fill = text_color,font=Font3)
            draw.text((15,init_y+4*high+margin), u"5. Timer", fill = text_color,font=Font3) #修改一下
            draw.text((15,init_y+5*high+margin), u"6. Emoji", fill = text_color,font=Font3)
            batteray_level = by + 4 + 0.26*(100-batteray)
            draw.rectangle([(bx, by), (bx + 20, by + 30)], fill = text_color, outline=None)
            draw.rectangle([(bx+5, by-4), (bx + 15, by)], fill = text_color, outline=None)
            draw.rectangle([(bx+4, by+4), (bx + 16, batteray_level)], fill = background_color, outline=None)

            image1=image1.rotate(0)
            disp.ShowImage(image1)
        state = counter
    elif state == counter:
        # print("stanby")

        image1 = Image.new("RGB", (disp.height,disp.width ), "WHITE")
        draw = ImageDraw.Draw(image1)
        # level = 14 + (high*1.05+margin)*(state%6)
        level = 18 + (state%6)*high
        draw.rectangle([(0, 0), (2000, 2000)], fill = background_color, outline=None)

        draw.rectangle([(0, level), (2000, level+high+margin)], fill = rectangle_color, outline=None)
        # draw.line([(0, 0), (0, 240)], fill = rectangle_color, width = 95)

        draw.text((15,init_y), u"1. CPU Usage", fill = text_color,font=Font3)
        draw.text((15,init_y+high+margin), u"2. Memory Utilization", fill = text_color,font=Font3)
        draw.text((15,init_y+2*high+margin), u"3. Current Time", fill = text_color,font=Font3)
        draw.text((15,init_y+3*high+margin), u"4. Network", fill = text_color,font=Font3)
        draw.text((15,init_y+4*high+margin), u"5. Timer", fill = text_color,font=Font3)
        draw.text((15,init_y+5*high+margin), u"6. Emoji", fill = text_color,font=Font3)

        
        batteray_level = by+ 4 + math.floor(0.26*(100-batteray))
        # batteray_level = by + 0.26*(100-48)
        
        draw.rectangle([(bx, by), (bx + 20, by + 30)], fill = text_color, outline=None)
        draw.rectangle([(bx+5, by-4), (bx + 15, by)], fill = text_color, outline=None)
        draw.rectangle([(bx+4, by+4), (bx + 16, batteray_level)], fill = background_color, outline=None)
        image1.save(f"./rubbish/kk4.jpg", "JPEG")

        image1=image1.rotate(0)
        disp.ShowImage(image1)
    else:
        print("pass")

    
    # time.sleep(0.1)

