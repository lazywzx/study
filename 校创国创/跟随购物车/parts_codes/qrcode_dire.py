import numpy as np
import cv2
import serial
import time
from pyzbar import pyzbar
import argparse

try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
except:
    print('Port Not Found!')


ap = argparse.ArgumentParser()

ap.add_argument("-o", "--output", type=str, default="content.csv",
                help="path to output csv file containing barcode")
args = vars(ap.parse_args())

vs = cv2.VideoCapture(0)
vs.set(3, 320)
vs.set(4, 240)

time.sleep(2.0)

csv = open(args["output"], "w")
found = set()

while True:
    qrcode = 0
    ret, frame = vs.read()
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        qrcode = barcodeData
    if qrcode != 0:
        print('xlabel:', x)
        if x <= 50:
            print('left')
            ser.write('H'.encode("gbk"))
        elif x <= 180:
            if w > 120:
                print('backward')
                ser.write('E'.encode("gbk"))
            elif w > 50:
                print('stop')
                ser.write('Z'.encode("gbk"))
            else:
                print('forward')
                ser.write('A'.encode("gbk"))
        else:
            print('right')
            ser.write('B'.encode("gbk"))
    else:
        print('stop')
        ser.write('Z'.encode("gbk"))
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
