import cv2
import numpy as np
#均值濾波器(低通濾波器)
#取附近像素的平均值計算
src=cv2.imread("t1.jpg")
dst1=cv2.blur(src,(3,3))
dst2=cv2.blur(src,(7,7))

#方框濾波器
#控制數值在0~255之間(沒有特別去定義，只是盡可能避免溢出)
#normalize=1:歸一化，反之
#輸出像素值 = 核內所有像素值的總和 / 核大小(中心點)
cst1=cv2.boxFilter(src,-1,(3,3),normalize=0)
cst2=cv2.boxFilter(src,-1,(7,7),normalize=1)


cv2.imshow("img",src)
cv2.imshow("d1",dst1)
cv2.imshow("d2",dst2)

cv2.imshow("cst1",cst1)
cv2.imshow("cst2",cst2)

cv2.waitKey(0)
cv2.destroyAllWindows()