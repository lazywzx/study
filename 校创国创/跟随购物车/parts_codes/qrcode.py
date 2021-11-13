from pyzbar import pyzbar
import argparse
import time
import cv2

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
        # barcodeType = barcode.type

        # text = "{}({})".format(barcodeData, barcodeType)
        qrcode = barcodeData

    if qrcode != 0:
        print('内容:', qrcode)
        print('宽度为:', w)
        print('横坐标:', x)

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.release()
cv2.destroyAllWindows()
