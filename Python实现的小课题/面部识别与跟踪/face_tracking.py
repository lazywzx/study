#!/usr/bin/env python2
# from __future__ import division
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 320)
#face.xml的位置要和本程序位于同一文件夹下
face_cascade = cv2.CascadeClassifier( 'eye.xml' )

while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #要先将每一帧先转换成灰度图，在灰度图中进行查找
    faces = face_cascade.detectMultiScale( gray )
    if len(faces)>0:
        print('face found!')
        for (x,y,w,h) in faces:
            #参数分别是“目标帧”，“矩形”，“矩形大小”，“线条颜色”，“宽度”
            cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)

    cv2.imshow("capture", frame)
    if cv2.waitKey(1)==119:
        print('cut')
    
cap.release()
cv2.destroyAllWindows()
