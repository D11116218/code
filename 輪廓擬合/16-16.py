import cv2
import numpy as np


src=cv2.imread("3.jpg")
gray_src=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
ret,dst_binary=cv2.threshold(gray_src,175,255,cv2.THRESH_BINARY)
contours,hierarchy=cv2.findContours(dst_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

h=len(contours)
for i in range(h):
    hull=cv2.convexHull(contours[0])
    dst=cv2.polylines(src,[hull],True,(0,255,0),2)


cv2.imshow("dst",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()