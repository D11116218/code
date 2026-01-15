import cv2
import numpy as np

src=cv2.imread("c.jpg")
src_gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
#二值化
ret, dst_binary=cv2.threshold(src_gray,175,255,cv2.THRESH_BINARY)
#輪廓
contours, hierarchy=cv2.findContours(dst_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
n=len(contours)
src1=src.copy()
src2=src.copy()
for i in range(n):
    approx=cv2.approxPolyDP(contours[i],3,True)
    dst1=cv2.polylines(src1,[approx],True,(0,255,0),2)
    approx=cv2.approxPolyDP(contours[i],15,True)
    dst2=cv2.polylines(src2,[approx],True,(0,255,0),2)
cv2.imshow("src1",src1)
cv2.imshow("src2",src2)

cv2.waitKey(0)
cv2.destroyAllWindows()