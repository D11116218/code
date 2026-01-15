import cv2
import numpy as np
#圓形_最小包圍物體
src=cv2.imread("c.jpg")
src_gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
ret,dst_binary=cv2.threshold(src_gray,127,255,cv2.THRESH_BINARY)
contours,hierarchy=cv2.findContours(dst_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
(x,y),radius=cv2.minEnclosingCircle(contours[0])#最小外接圓
center=(int(x),int(y))#中心點
radius=int(radius)
dst=cv2.circle(src,center,radius,(0,0,255),2)#原圖、中心點、半徑、顏色、線寬

cv2.namedWindow("src",cv2.WINDOW_NORMAL)
cv2.namedWindow("dst",cv2.WINDOW_NORMAL)
cv2.imshow("src",src)
cv2.imshow("dst",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()