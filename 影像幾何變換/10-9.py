import cv2
import numpy as np

#影像平移

src=cv2.imread("t1.jpg")
cv2.imshow("src",src)

height,width=src.shape[0:2]
dsize=(width,height)
x=50
y=100
#M矩陣公式取得
M=np.float32([[1,0,x]#控制水平方向(x軸)
             ,[0,1,y]])#控制垂直方向(y軸)
dst=cv2.warpAffine(src,M,dsize)
cv2.imshow("Dst",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()