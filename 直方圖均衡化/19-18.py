import cv2

src=cv2.imread("t1.jpg",cv2.IMREAD_COLOR)
cv2.imshow("src",src)
(b,g,r)=cv2.split(src)#分割通道
blue=cv2.equalizeHist(b)#藍色通道均衡化
green=cv2.equalizeHist(g)#綠色通道均衡化
red=cv2.equalizeHist(r)#紅色通道均衡化
dst=cv2.merge((blue,green,red))#合併通道
cv2.imshow("dst",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()