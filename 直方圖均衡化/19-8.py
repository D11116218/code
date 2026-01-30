import cv2
import matplotlib.pyplot as plt
#直方圖均衡化

src=cv2.imread("e.jpg",cv2.IMREAD_COLOR)
cv2.imshow("src",src)
b=cv2.calcHist([src],[0],None,[256],[0,256])#B 通道統計資料
g=cv2.calcHist([src],[1],None,[256],[0,256])#G 通道統計資料
r=cv2.calcHist([src],[2],None,[256],[0,256])#R 通道統計資料

plt.plot(b, color="blue",label="B channel")#用plot繪製B通道
plt.plot(g, color="green",label="G channel")#用plot繪製G通道
plt.plot(r, color="red",label="R channel")#用plot繪製R通道
plt.legend(loc="best")
plt.show()