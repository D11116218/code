import cv2
import numpy as np

src=cv2.imread("t1.jpg")
cv2.imshow("A1",src)

height,width=src.shape[0:2]
#重新定義四個點座標
a1=[0,0]#左上角 
b1=[width,0]#右上角 
c1=[0,height]#左下角 
d1=[width-1,height-1]#右下角 
srcp=np.float32([a1,b1,c1,d1])#定義scep的四個點

a2=[150,0]#左上角向右移 (像素)
b2=[width-150,0]#右上角向右移 (像素)
c2=[0,height-1]#左下角向右移 (像素)
d2=[width-1,height-1]#右下角向右移 (像素)
dstp=np.float32([a2,b2,c2,d2])

M=cv2.getPerspectiveTransform(srcp,dstp)#取得透視變換矩陣
dsize=(width,height)
dst=cv2.warpPerspective(src,M,dsize)#用M對src進行變換
cv2.imshow("Dst",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()