import cv2
import numpy as np
#影像仿射，影像傾斜
src=cv2.imread("t1.jpg")
cv2.imshow("A1",src)
height,width=src.shape[0:2]#取得高、寬
srcp=np.float32([[0,0],[width-1,0],[0,height-1]])#原圖三個點
#重新定義三個點座標
a=[0,height*0.2]
b=[width*0.5,height*0.2]
c=[width*0.3,height*0.9]
dstp=np.float32([a,b,c])

M=cv2.getAffineTransform(srcp,dstp)#回傳變換矩陣
dsize=(width,height)
dst=cv2.warpAffine(src,M,dsize)#用M對src進行變換
cv2.imshow("A2",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()