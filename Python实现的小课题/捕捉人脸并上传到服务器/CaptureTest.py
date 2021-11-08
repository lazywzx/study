#!/usr/bin/python3
import cv2
from FTPTest import SSHConnection

# 捕捉摄像头视频流
capture = cv2.VideoCapture(0)
capture.set(3, 320)
capture.set(4, 320)
#eye.xml的位置要和本程序位于同一文件夹下
face_cascade = cv2.CascadeClassifier('face.xml')


#函数用于人脸识别与保存
def face_tracking():
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 要先将每一帧先转换成灰度图，在灰度图中进行查找
    faces = face_cascade.detectMultiScale(gray)

    if len(faces) > 0:
        print('found')
        for (x, y, w, h) in faces:
            # 参数分别是“目标帧”，“矩形”，“矩形大小”，“线条颜色”，“宽度”
            cv2.rectangle(frame, (x, y), (x + h, y + w), (0, 255, 0), 2)
        cv2.imwrite("capture.png", frame)  # 保存
        return 'found'
    else:
        print('not found')
        return 'not found'


while True:
    isfound = face_tracking()
    if isfound == 'found':
        break

# 上传到服务器
ssh = SSHConnection()
ssh.connect()
ssh.upload('./capture.png', '/root/IoT/capture.png')
print('upload successful')

capture.release()	 # 释放摄像头

while True:
    reuslt = ssh.cmd('ls /root/IoT/result.txt')
    if reuslt != '':
        print('exist')
        ssh.download('/root/IoT/result.txt', './result.txt')
        print('download successful')
        # 分析result.txt文件决定报警/开锁
        break
    else:
        print('not exist')

ssh.close()
