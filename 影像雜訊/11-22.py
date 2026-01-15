import cv2
import numpy as np
#雙邊濾波器
#保留影像邊緣防止模糊
src=cv2.imread("t1.jpg")
dst1=cv2.blur(src,(5,5))#均值濾波
dst2=cv2.boxFilter(src,-1,(5,5),normalize=0)#方框濾波
dst3=cv2.medianBlur(src,5)#中值濾波
dst4=cv2.GaussianBlur(src,(5,5),0,0)#高斯濾波
dst5=cv2.bilateralFilter(src,15,100,100)#雙邊濾波

src=cv2.imshow("src",src)
dst1=cv2.imshow("dst1",dst1)
dst2=cv2.imshow("dst2",dst2)
dst3=cv2.imshow("dst3",dst3)
dst4=cv2.imshow("dst4",dst4)
dst5=cv2.imshow("dst5",dst5)

cv2.waitKey(0)
cv2.destroyAllWindows()



