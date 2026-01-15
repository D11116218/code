import cv2
import numpy as np
src=cv2.imread("t1.jog")
#中值濾波器
#去除較大的黑白亮點(噪點)
#取單位像素的中值(非像素值)
dst1=cv2.medianBlur(src,3)#濾波核大小範圍，平滑效果越強，模糊程度越大
dst2=cv2.medianblur(src,5)
dst3=cv2.medianblur(src,7)
cv2.imshow("src",src)
cv2.imshow("dst1",dst1)
cv2.imshow("dst2",dst2)
cv2.imshow("dst3",dst3)
cv2.waitKey(0)
cv2.destroyAllWindows()