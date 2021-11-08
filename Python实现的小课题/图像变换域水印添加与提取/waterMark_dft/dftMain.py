# -*- coding:utf-8 -*-
import sys
sys.path.append('../')
import attack
import psnr
import cv2
import dftWM

# Path
orilzu = "./images/original/lzu.jpeg"
oriwm = "./images/original/watermark.png"

# embedded
grayimg, wmimg, orimag, wmmag, oricopymag, recoverImg = dftWM.DFTEmbdWM(orilzu, oriwm, 256)
# write
cv2.imwrite("./images/embedded/grayimg.jpeg", grayimg)
cv2.imwrite("./images/embedded/wmimg.png", wmimg)
cv2.imwrite("./images/embedded/orimag.jpeg", orimag)
cv2.imwrite("./images/embedded/wmmag.png", wmmag)
cv2.imwrite("./images/embedded/embdmag.jpeg", oricopymag)
cv2.imwrite("./images/embedded/recoverImg.jpeg", recoverImg)

# PSNR
print(psnr.psnr1(grayimg, recoverImg))

# attack
addnoise = attack.addNoise(recoverImg, 0.01)
rotate = attack.imgRotate(recoverImg, 0.1)
cut = attack.imgCut(recoverImg, 50, 200, 50, 200, fill=0)
# write
cv2.imwrite("./images/attack/addnoise.jpeg", addnoise)
cv2.imwrite("./images/attack/rotate.jpeg", rotate)
cv2.imwrite("./images/attack/cut.jpeg", cut)

# extract
extractNoAttack = dftWM.DFTExttWM(orilzu, oriwm, "./images/embedded/recoverImg.jpeg", 256)
extractAddNoise = dftWM.DFTExttWM(orilzu, oriwm, "./images/attack/addnoise.jpeg", 256)
extractRotate = dftWM.DFTExttWM(orilzu, oriwm, "./images/attack/rotate.jpeg", 256)
extractCut = dftWM.DFTExttWM(orilzu, oriwm, "./images/attack/cut.jpeg", 256)
# write
cv2.imwrite("./images/extract/extractNoAttack.png", extractNoAttack)
cv2.imwrite("./images/extract/extractAddNoise.png", extractAddNoise)
cv2.imwrite("./images/extract/extractRotate.png", extractRotate)
cv2.imwrite("./images/extract/extractCut.png", extractCut)
