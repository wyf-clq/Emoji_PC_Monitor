import os
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
# intialize MPU sensor
import pickle

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus = smbus.SMBus(1) 
address = 0x68       
bus.write_byte_data(address, power_mgmt_1, 0)
total = [0]*5
emoji_event = False

def MPU_DETECT():
    global total, MPU_state, emoji_event
    while True:
        a = read_word_2c(0x43)
        b = read_word_2c(0x45)
        c = read_word_2c(0x47)

        total_number = math.sqrt(a**2+b**2+c**2)
        # print(total)
        total.insert(0,total_number)
        total.pop()

        MPU_state = sum(total)/5
        print(MPU_state)

       

# 假设这是你想存储的变量

        # 使用 pickle 将变量存储到文件
        with open('mpu_EVENT.pkl', 'wb') as file:
            pickle.dump(MPU_state, file)

        time.sleep(0.2)


MPU_DETECT()