# -*- coding:utf-8 -*-
import sys
sys.path.append('../')
import attack
import psnr
import cv2
import dwtWM

# Path
orilzu = "./images/original/lzu.jpeg"
oriwm = "./images/original/watermark.png"

# embedded
grayimg, waterMark, dwtresult, embddwtresult, embeddedImage = dwtWM.DWTEmbdWM(orilzu, oriwm, 0.2)
# write
cv2.imwrite("./images/embedded/grayimg.jpeg", grayimg)
cv2.imwrite("./images/embedded/wm.png", waterMark)
cv2.imwrite("./images/embedded/imgdwt.jpeg", dwtresult)
cv2.imwrite("./images/embedded/embdimgdwt.jpeg", embddwtresult)
cv2.imwrite("./images/embedded/embeddedWaterMark.jpeg", embeddedImage)

# PSNR
print(psnr.psnr1(grayimg, embeddedImage))

# attack
addnoise = attack.addNoise(embeddedImage, 0.01)
rotate = attack.imgRotate(embeddedImage, 0.1)
cut = attack.imgCut(embeddedImage, 50, 200, 50, 200, fill=0)
# write
cv2.imwrite("./images/attack/addnoise.jpeg", addnoise)
cv2.imwrite("./images/attack/rotate.jpeg", rotate)
cv2.imwrite("./images/attack/cut.jpeg", cut)

# extract
extractNoAttack = dwtWM.DWTExttWM(orilzu, "./images/embedded/embeddedWaterMark.jpeg", 0.2)
extractAddNoise = dwtWM.DWTExttWM(orilzu, "./images/attack/addnoise.jpeg", 0.2)
extractRotate = dwtWM.DWTExttWM(orilzu, "./images/attack/rotate.jpeg", 0.2)
extractCut = dwtWM.DWTExttWM(orilzu, "./images/attack/cut.jpeg", 0.2)
# write
cv2.imwrite("./images/extract/extractNoAttack.png", extractNoAttack)
cv2.imwrite("./images/extract/extractAddNoise.png", extractAddNoise)
cv2.imwrite("./images/extract/extractRotate.png", extractRotate)
cv2.imwrite("./images/extract/extractCut.png", extractCut)
