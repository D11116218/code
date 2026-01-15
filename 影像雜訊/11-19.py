import cv2
import numpy as np
src=cv2.imread("t1.jpg")
#高斯濾波器
dst1=cv2.GaussianBlur(src,(3,3),0,0)
dst2=cv2.GaussianBlur(src,(5,5),1,3)
dst3=cv2.GaussianBlur(src,(29,29),25,25)
#越靠近濾波核心，權重越高
#(5,5) 為濾波核的大小(正方形)
#,0,0 為x軸、y軸方向模糊
#將濾波核周圍乘以權重相加，得出濾波核核心值
dst1=cv2.imshow("dst1",src)
dst2=cv2.imshow("dst2",dst2)
dst3=cv2.imshow("dst3",dst3)

cv2.waitKey(0)
cv2.destroyAllWindows()