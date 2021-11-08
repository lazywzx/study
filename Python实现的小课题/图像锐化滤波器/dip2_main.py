import matplotlib.pyplot as plt
import dip2_functions as df

path = './d.jpg'
image, btwsres, binary, morp = df.ColorImageBorder(path, color=False)

# 绘图时显示中文字体
plt.rcParams['font.sans-serif'] = ['FangSong']
plt.rcParams['axes.unicode_minus'] = False

plt.subplot(141), plt.imshow(image, 'gray'), plt.title('原始图像'), plt.xticks([]), plt.yticks([])
plt.subplot(142), plt.imshow(btwsres, 'gray'), plt.title('锐化滤波'), plt.xticks([]), plt.yticks([])
plt.subplot(143), plt.imshow(binary, 'gray'), plt.title('二值化'), plt.xticks([]), plt.yticks([])
plt.subplot(144), plt.imshow(morp, 'gray'), plt.title('形态学处理'), plt.xticks([]), plt.yticks([])
plt.show()
