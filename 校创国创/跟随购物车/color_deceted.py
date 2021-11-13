import numpy as np
import cv2
import serial

try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
except:
    print('Port Not Found!')

blue_lower = np.array([100, 43, 46])
blue_upper = np.array([124, 255, 255])

cap = cv2.VideoCapture(0)

cap.set(3, 320)
cap.set(4, 240)


def color_follow():
    ret, frame = cap.read()
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    x_position = 330
    # blue
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    # 图像学膨胀腐蚀
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    # 寻找轮廓并绘制轮廓
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        # 寻找面积最大的轮廓并画出其最小外接圆
        cnt = max(cnts, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        print(radius)
        cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 255), 2)
        # 找到物体的位置坐标
        x_position = int(x)
        print(x_position)

        if x_position <= 66:
            print('left')
            ser.write('H'.encode("gbk"))
        elif x_position <= 254:
            print('forward')
            if radius > 30:
                print('backward')
                ser.write('E'.encode("gbk"))
            elif radius > 13:
                print('stop')
                ser.write('Z'.encode("gbk"))
            else:
                ser.write('A'.encode("gbk"))
        elif x_position <= 320:
            print('right')
            ser.write('B'.encode("gbk"))
        else:
            print('stop')
            ser.write('Z'.encode("gbk"))
    else:
        print('stop')
        ser.write('Z'.encode("gbk"))

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('key_kill')


