#!/usr/bin/python

import pygame, sys
from pygame.locals import *
import RPi.GPIO as GPIO
import socket
import smbus
import math
import os
import time

def read_all(add):
    raw_gyro_data = bus.read_i2c_block_data(add, 0x43, 6)
    raw_accel_data = bus.read_i2c_block_data(add, 0x3b, 6)

    gyro_scaled_x = twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / gyro_scale
    gyro_scaled_y = twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / gyro_scale
    gyro_scaled_z = twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / gyro_scale
 
    accel_scaled_x = twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / accel_scale
    accel_scaled_y = twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / accel_scale
    accel_scaled_z = twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / accel_scale
    
    return(gyro_scaled_x,gyro_scaled_y,gyro_scaled_z,accel_scaled_x,accel_scaled_y,accel_scaled_z)
#==========================================================
def read_all_1(line):
    
    gyro_scaled_x = line[0] / gyro_scale
    gyro_scaled_y = line[1] / gyro_scale
    gyro_scaled_z = line[2] / gyro_scale
 
    accel_scaled_x = line[3]
    accel_scaled_y = line[4]
    accel_scaled_z = line[5]
    
    return(gyro_scaled_x,gyro_scaled_y,gyro_scaled_z,accel_scaled_x,accel_scaled_y,accel_scaled_z)
#==========================================================
def twos_compliment(val):

    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def dist(a, b):
    return math.sqrt((a * a) + (b * b))

def read_sensor(number_of_sensor):
    if number_of_sensor == 1:
        GPIO.output(17, GPIO.LOW)
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(22, GPIO.HIGH)
    elif number_of_sensor == 2:
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(22, GPIO.HIGH)
    elif number_of_sensor == 3:
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(22, GPIO.LOW)
        pass

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
#==================================
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
gyro_scale = 131.0
accel_scale = 16384.0
 
address = 0x68  # This is the default I2C address of ITG-MPU breakout board
address2 = 0x69  
pygame.init()
pi = 3.14
s2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDP_IP = "10.42.0.1"
UDP_PORT = 12345                
UDP_IP2 = "192.168.43.161"
UDP_PORT2= 5001
s2.sendto("Moha", (UDP_IP, UDP_PORT))
while True:
    recvd,addr = s2.recvfrom(1024)
    recvd1 = recvd.strip()
    print recvd1
    if recvd1 == "RealTime" or recvd1 == "Simulation":
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(22, GPIO.HIGH)
        bus = smbus.SMBus(1)  # SMBus(1) for Raspberry pi 2 board
        adress = 0x68

        # Now wake the 6050 up as it starts in sleep mode
        bus.write_byte_data(address, power_mgmt_1, 0)
        bus.write_byte_data(address2, power_mgmt_1, 0)
        now = time.time()
         
        K = 0.98
        K1 = 1 - K
        time_diff = 0.01
        ################# 1 #########################
        read_sensor(1)
        (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all(address)
        last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        gyro_offset_x = gyro_scaled_x
        gyro_offset_y = gyro_scaled_y
        gyro_total_x = (last_x) - gyro_offset_x
        gyro_total_y = (last_y) - gyro_offset_y
#        time.sleep(1)
        ################### 2 ###############
        read_sensor(2)
        (gyro_scaled_x2, gyro_scaled_y2, gyro_scaled_z2, accel_scaled_x2, accel_scaled_y2, accel_scaled_z2) = read_all(address)
        last_x2 = get_x_rotation(accel_scaled_x2, accel_scaled_y2, accel_scaled_z2)
        last_y2 = get_y_rotation(accel_scaled_x2, accel_scaled_y2, accel_scaled_z2)

        gyro_offset_x2 = gyro_scaled_x2
        gyro_offset_y2 = gyro_scaled_y2
        gyro_total_x2 = (last_x2) - gyro_offset_x2
        gyro_total_y2 = (last_y2) - gyro_offset_y2
#        time.sleep(1)
        ############### 3 #####################

        read_sensor(3)
        (gyro_scaled_x3, gyro_scaled_y3, gyro_scaled_z3, accel_scaled_x3, accel_scaled_y3, accel_scaled_z3) = read_all(address)
        last_x3 = get_x_rotation(accel_scaled_x3, accel_scaled_y3, accel_scaled_z3)
        last_y3 = get_y_rotation(accel_scaled_x3, accel_scaled_y3, accel_scaled_z3)

        gyro_offset_x3 = gyro_scaled_x3
        gyro_offset_y3 = gyro_scaled_y3
        gyro_total_x3 = (last_x3) - gyro_offset_x3
        gyro_total_y3 = (last_y3) - gyro_offset_y3
#        time.sleep(1)

        #========================
        while True:
            ################## 1 #########################################3
            time.sleep(time_diff - 0.005)
            read_sensor(1)

            (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all(address)
            
            gyro_scaled_x -= gyro_offset_x
            gyro_scaled_y -= gyro_offset_y
             
            gyro_x_delta = (gyro_scaled_x * time_diff)
            gyro_y_delta = (gyro_scaled_y * time_diff)

            gyro_total_x += gyro_x_delta
            gyro_total_y += gyro_y_delta

            rotation_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
            rotation_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
         
            last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
            last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)
            
            
            delta_y = math.radians(last_y)
            delta_x = math.radians(last_x)

            flag = 0
            if(accel_scaled_y >= 0 and accel_scaled_z >= 0) or (accel_scaled_y < 0 and accel_scaled_z >= 0):
                flag = 0
            else:
                flag = 1
            if(delta_y > 0 and not(flag)):
                delta_y = delta_y
                delta_x = delta_x
            elif((delta_y > 0) and flag):    
                delta_y = -(delta_y) + pi
                delta_x = -(delta_x) + pi
            elif((delta_y < 0) and not(flag)):    
                delta_y = delta_y + 2*pi
                delta_x = delta_x + 2*pi
            elif((delta_y < 0) and flag):    
                delta_y = -(delta_y) + pi
                delta_x = -(delta_x) + pi
            if delta_y > 2*pi:
                delta_y = delta_y - 2*pi
                delta_x = delta_x - 2*pi
#            time.sleep(.001)
            ####################################################

            ####################### 2 ##########################
            read_sensor(2)

            (gyro_scaled_x2, gyro_scaled_y2, gyro_scaled_z2, accel_scaled_x2, accel_scaled_y2, accel_scaled_z2) = read_all(address)
            
            gyro_scaled_x2 -= gyro_offset_x2
            gyro_scaled_y2 -= gyro_offset_y2
             
            gyro_x_delta2 = (gyro_scaled_x2 * time_diff)
            gyro_y_delta2 = (gyro_scaled_y2 * time_diff)

            gyro_total_x2 += gyro_x_delta2
            gyro_total_y2 += gyro_y_delta2

            rotation_x2 = get_x_rotation(accel_scaled_x2, accel_scaled_y2, accel_scaled_z2)
            rotation_y2 = get_y_rotation(accel_scaled_x2, accel_scaled_y2, accel_scaled_z2)
         
            last_x2 = K * (last_x2 + gyro_x_delta2) + (K1 * rotation_x2)
            last_y2 = K * (last_y2 + gyro_y_delta2) + (K1 * rotation_y2)
            
            
            delta_y2 = math.radians(last_y2)
            delta_x2 = math.radians(last_x2)

            flag = 0
            if(accel_scaled_y2 >= 0 and accel_scaled_z2 >= 0) or (accel_scaled_y2 < 0 and accel_scaled_z2 >= 0):
                flag = 0
            else:
                flag = 1
            if(delta_y2 > 0 and not(flag)):
                delta_y2 = delta_y2
                delta_x2 = delta_x2
            elif((delta_y2 > 0) and flag):    
                delta_y2 = -(delta_y2) + pi
                delta_x2 = -(delta_x2) + pi
            elif((delta_y2 < 0) and not(flag)):    
                delta_y2 = delta_y2 + 2*pi
                delta_x2 = delta_x2 + 2*pi
            elif((delta_y2 < 0) and flag):    
                delta_y2 = -(delta_y2) + pi
                delta_x2 = -(delta_x2) + pi
            if delta_y2 > 2*pi:
                delta_y2 = delta_y2 - 2*pi
                delta_x2 = delta_x2 - 2*pi
#            time.sleep(.001)
        ###########################################################

        ################### 3 ###############################
            read_sensor(3)

            (gyro_scaled_x3, gyro_scaled_y3, gyro_scaled_z3, accel_scaled_x3, accel_scaled_y3, accel_scaled_z3) = read_all(address)
            
            gyro_scaled_x3 -= gyro_offset_x3
            gyro_scaled_y3 -= gyro_offset_y3
             
            gyro_x_delta3 = (gyro_scaled_x3 * time_diff)
            gyro_y_delta3 = (gyro_scaled_y3 * time_diff)

            gyro_total_x3 += gyro_x_delta3
            gyro_total_y3 += gyro_y_delta3

            rotation_x3 = get_x_rotation(accel_scaled_x3, accel_scaled_y3, accel_scaled_z3)
            rotation_y3 = get_y_rotation(accel_scaled_x3, accel_scaled_y3, accel_scaled_z3)
         
            last_x3 = K * (last_x3 + gyro_x_delta3) + (K1 * rotation_x3)
            last_y3 = K * (last_y3 + gyro_y_delta3) + (K1 * rotation_y3)
            
            
            delta_y3 = math.radians(last_y3)
            delta_x3 = math.radians(last_x3)

            flag = 0
            if(accel_scaled_y3 >= 0 and accel_scaled_z3 >= 0) or (accel_scaled_y3 < 0 and accel_scaled_z3 >= 0):
                flag = 0
            else:
                flag = 1
            if(delta_y3 > 0 and not(flag)):
                delta_y3 = delta_y3
                delta_x3 = delta_x3
            elif((delta_y3 > 0) and flag):    
                delta_y3 = -(delta_y3) + pi
                delta_x3 = -(delta_x3) + pi
            elif((delta_y3 < 0) and not(flag)):    
                delta_y3 = delta_y3 + 2*pi
                delta_x3 = delta_x3 + 2*pi
            elif((delta_y3 < 0) and flag):    
                delta_y3 = -(delta_y3) + pi
                delta_x3 = -(delta_x3) + pi
            if delta_y3 > 2*pi:
                delta_y3 = delta_y3 - 2*pi
                delta_x3 = delta_x3 - 2*pi
#            time.sleep(.001)
        #################################################################
         
            string1 = str(delta_x)
            string2 = str(delta_x2)
            string3 = str(delta_x3)
            string4 = str(delta_y3)
            string5 = str(last_x)
            string5 = string5[:5]
            string6 = str(last_x2)
            string6 = string6[:5]
            string7 = str(last_x3)
            string7 = string7[:5]
            string8 = str(last_y3)
            string8 = string8[:5]
            if recvd1 == "RealTime":
                s2.sendto("x1"+string5.encode(), (UDP_IP2, UDP_PORT2))
                s2.sendto("x2"+string6.encode(), (UDP_IP2, UDP_PORT2))
                s2.sendto("x3"+string7.encode(), (UDP_IP2, UDP_PORT2))
                s2.sendto("y3"+string8.encode(), (UDP_IP2, UDP_PORT2))
            else:
                s2.sendto("x1"+string1.encode(), (UDP_IP, UDP_PORT))
                s2.sendto("x2"+string2.encode(), (UDP_IP, UDP_PORT))
                s2.sendto("x3"+string4.encode(), (UDP_IP, UDP_PORT))
                s2.sendto("y3"+string3.encode(), (UDP_IP, UDP_PORT))
            if recvd1 == "Simulation":
                recvd3,addr = s2.recvfrom(1024)
                if recvd3 == "StopSim":
                    break
    elif recvd1 == "Exit":
        s2.close()
        break