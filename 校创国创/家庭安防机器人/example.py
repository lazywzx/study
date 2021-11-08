#手机服务器的ip地址,可以在App上查到
server_ip = '192.168.43.69'
# 导入客户端文件
import client
from datetime import datetime


import os
import RPi.GPIO as GPIO
import time
import serial
import pygame
import cv2

#创建客户端对象，用于连接手机，需要传入服务器手机IP地址
client_w = client.Client(server_ip)
#开始连接手机，如果连接成功，手机会有显示，之所以创建对象和
#连接分开是因为，连接是有可能断开的，这是只需要重新连接即可，
#而不需要创建对象
client_w.connectServer()
try:
    ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
except Exception as e:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)


############################人脸检测###################################
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 320)
#face.xml的位置要和本程序位于同一文件夹下
face_cascade = cv2.CascadeClassifier( 'eye.xml' )

def face_tracking():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 要先将每一帧先转换成灰度图，在灰度图中进行查找
    faces = face_cascade.detectMultiScale(gray)
    if len(faces) > 0:
        messeg = 'face found!'
        for (x, y, w, h) in faces:
            # 参数分别是“目标帧”，“矩形”，“矩形大小”，“线条颜色”，“宽度”
            cv2.rectangle(frame, (x, y), (x + h, y + w), (0, 255, 0), 2)
    else:
        messeg = 'not found!'

    cv2.imshow("capture", frame)
    if cv2.waitKey(1) == 119:
        print('cut')
    return messeg


pygame.mixer.init()
def face_alarm(result):
    if result == 'face found!':
        print('face_start')
        ser.write('3'.encode("gbk"))  # 停止
        print('停止')
        client_w.send('Stranger!')
        print('stranger')
        
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 要先将每一帧先转换成灰度图，在灰度图中进行查找
        faces = face_cascade.detectMultiScale(gray)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # 参数分别是“目标帧”，“矩形”，“矩形大小”，“线条颜色”，“宽度”
                cv2.rectangle(frame, (x, y), (x + h, y + w), (0, 255, 0), 2)

        cv2.imshow("capture", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q') or True:
            cv2.imwrite('face_photo.jpg', frame)
            client_w.sendImage('face_photo.jpg')
        pygame.mixer.music.load('person_alarm.mp3')
        pygame.mixer.music.play()
        time.sleep(3)
        print('face_end')


############################温度检测###################################
device_file = '/sys/bus/w1/devices/28-52b5f71d64ff/w1_slave'
def read_temp_raw():
    f = open(device_file,'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.0
    return temp_c

def temp_alarm(temp_num):
    if temp_num > 22:
        ser.write('3'.encode("gbk"))  # 停止
        print('停止')
        client_w.send('Heat!')
        client_w.send(temp_num)  # 发送温度到手机
        pygame.mixer.music.load('temp_alarm.mp3')
        pygame.mixer.music.play()
        time.sleep(3)


#######################超声波测距#######################################
def check_distance(TRIG, ECHO):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, True)
    time.sleep(0.000015)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pass

    pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pass

    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print("Distance: {}cm".format(distance))
    GPIO.cleanup()
    return format(distance)


def read_sr04():
    """读取超声波数据"""
    left_distance = float(check_distance(23, 24))
    right_distance = float(check_distance(27, 22))

    if left_distance < 50 and right_distance < 50:
        ser.write('3'.encode("gbk"))  # 停止
        print('停止')
        ser.write('2'.encode("gbk"))
        time.sleep(1)
        ser.write('4'.encode("gbk"))
        time.sleep(4)
    elif left_distance < 50:
            ser.write('5'.encode("gbk"))  # 右转
            print('右转')
    elif right_distance < 50:
            ser.write('4'.encode("gbk"))  # 左转
            print('左转')
    else:
        ser.write('1'.encode("gbk"))    # 前进
        print('前进')


def fire_alarm():
    client_w.send('Fire!')
    
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 要先将每一帧先转换成灰度图，在灰度图中进行查找
    faces = face_cascade.detectMultiScale(gray)
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            # 参数分别是“目标帧”，“矩形”，“矩形大小”，“线条颜色”，“宽度”
            cv2.rectangle(frame, (x, y), (x + h, y + w), (0, 255, 0), 2)

    cv2.imshow("capture", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q') or True:
        cv2.imwrite('fire_photo.jpg', frame)
        client_w.sendImage('fire_photo.jpg')
    pygame.mixer.music.load('fire_alarm.mp3')
    pygame.mixer.music.play()
    time.sleep(2)

##函数介绍
#1.可以通过send函数直接发送一个字符串或者整数
# client_w.send('aaa')
#2.可以通过sendImage直接发送图片，参数是图片路径，注意后缀是JPG还是png
# client_w.sendImage('E:/test2.jpg')
#3.read函数获取手机消息，获取消息是异步的，使用后马上返回，如果有消息，
#则返回消息，如果没有消息则返回None
#注意这里可以编辑框发送，但下面有快捷按钮
#w键 发送 ‘w'，a键 发送 ‘a'  ，....，stop键发送'stop'
# msg = client_w.read()
# if msg == 'w':
#     print('有消息')
# elif msg == None:
#     print('无消息')

#4.client_w.isConnected()用于判断是否连接，连接成功返回true
#5.client_w.clearMessage()清空消息池的所有消息，因为按键有可能按了多次，但你只想收到一次就行了
#这是当接受一个消息时就可以选择清空所有消息

#使用示例
control_flag = 0
msg = 'e'
last_time = datetime.now()
while True:
    #     判断是否连接成功，好习惯就是每次循环都要判断是否连接成功
    if client_w.isConnected() == False:
        client_w.connectServer()
        continue
    #   每个while循环只需要读取一次就行了
    msg = client_w.read()
    print(msg)

    # 判断是否受控
    if msg != None:
        control_flag = 1

    # 决定运动状态
    if control_flag:
        if msg == 'w':
            print("向前")
            ser.write('1'.encode("gbk"))
        elif msg == 's':
            print('向后')
            ser.write('2'.encode("gbk"))
        elif msg == 'a':
            print('向左')
            ser.write('6'.encode("gbk"))
        elif msg == 'd':
            print('向右')
            ser.write('7'.encode("gbk"))
        elif msg == 'stop':
            print('停止')
            ser.write('3'.encode("gbk"))
        elif msg == 'f':    # 判断火灾
            print('fire')
            ser.write('3'.encode("gbk"))
            fire_alarm()
    else:
        # 乱走
        print('1')
        read_sr04()
        print('ok')
        # 判断有没有人
        face_result = face_tracking()
        print(face_result)
        if (datetime.now() - last_time).seconds > 1:
            face_alarm(face_result)
            last_time = datetime.now()
        # 测温度
        temp_num = read_temp()
        print(temp_num)
        temp_alarm(temp_num)
