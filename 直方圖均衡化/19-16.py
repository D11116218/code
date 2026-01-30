import cv2
import matplotlib.pyplot as plt
#直方圖均衡化
src=cv2.imread("e.jpg",cv2.IMREAD_GRAYSCALE)
plt.subplot(221)#建立子圖1
plt.imshow(src,'gray')
plt.subplot(222)#建立子圖2
plt.hist(src.ravel(),256)
plt.subplot(223)#建立子圖3
dst=cv2.equalizeHist(src)#直方圖均衡化
plt.imshow(dst,'gray')#顯示均值化影像
plt.subplot(224)#建立子圖4
plt.hist(dst.ravel(),256)
plt.show()