# -*- coding:utf-8 -*-
import sys
sys.path.append('../')
import attack
import psnr
import cv2
import dctWM

# Path
orilzu = "./images/original/lzu.jpeg"
oriwm = "./images/original/watermark.png"

# embedded
grayimg, watermark, oridctImg, dctwater, dctImg, idctImg = dctWM.DCTEmbdWM(orilzu, oriwm, 3, 3, 0.03)
# write
cv2.imwrite("./images/embedded/grayimg.jpeg", grayimg)
cv2.imwrite("./images/embedded/watermarkgray.png", watermark)
cv2.imwrite("./images/embedded/dctImg.jpeg", oridctImg)
cv2.imwrite("./images/embedded/dctwater.png", dctwater)
cv2.imwrite("./images/embedded/embddctimg.jpeg", dctImg)
cv2.imwrite("./images/embedded/idctimg.jpeg", idctImg)

# PSNR
print(psnr.psnr1(grayimg, idctImg))

# attack
addnoise = attack.addNoise(idctImg, 0.01)
rotate = attack.imgRotate(idctImg, 0.1)
cut = attack.imgCut(idctImg, 50, 200, 50, 200, fill=0)
# write
cv2.imwrite("./images/attack/addnoise.jpeg", addnoise)
cv2.imwrite("./images/attack/rotate.jpeg", rotate)
cv2.imwrite("./images/attack/cut.jpeg", cut)

# extract
extractNoAttack = dctWM.DCTExttWM(orilzu, "./images/embedded/idctimg.jpeg", oriwm, 3, 3, 0.03)
extractAddNoise = dctWM.DCTExttWM(orilzu, "./images/attack/addnoise.jpeg", oriwm, 3, 3, 0.03)
extractRotate = dctWM.DCTExttWM(orilzu, "./images/attack/rotate.jpeg", oriwm, 3, 3, 0.03)
extractCut = dctWM.DCTExttWM(orilzu, "./images/attack/cut.jpeg", oriwm, 3, 3, 0.03)
# write
cv2.imwrite("./images/extract/extractNoAttack.png", extractNoAttack)
cv2.imwrite("./images/extract/extractAddNoise.png", extractAddNoise)
cv2.imwrite("./images/extract/extractRotate.png", extractRotate)
cv2.imwrite("./images/extract/extractCut.png", extractCut)
