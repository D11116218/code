import cv2
import numpy as np

src=cv2.imread("c.jpg")
src_gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
#二值化
ret, dst_binary=cv2.threshold(src_gray,175,255,cv2.THRESH_BINARY)
#輪廓
contours, hierarchy=cv2.findContours(dst_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


n=len(contours)
#直接修改會覆蓋原圖
src1=src.copy()
src2=src.copy()
for i in range(n):#從編號0到n-1個輪廓處裡
    approx=cv2.approxPolyDP(contours[i],3,True)#誤差值3
    dst1=cv2.polylines(src1,[approx],True,(0,255,0),2)#綠色、粗細
    approx=cv2.approxPolyDP(contours[i],15,True)#誤差值15
    dst2=cv2.polylines(src2,[approx],True,(0,255,0),2)#綠色、粗細

cv2.namedWindow("src1",cv2.WINDOW_NORMAL)
cv2.namedWindow("src2",cv2.WINDOW_NORMAL)
cv2.imshow("src1",src1)
cv2.imshow("src2",src2)

cv2.waitKey(0)
cv2.destroyAllWindows()