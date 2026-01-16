import cv2
import numpy as np
#最小包圍矩形
src=cv2.imread("c.jpg",cv2.IMREAD_GRAYSCALE)

ret,dst_binary=cv2.threshold(src,175,255,cv2.THRESH_BINARY)
contours,hierarchy=cv2.findContours(dst_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

box=cv2.minAreaRect(contours[0])
print(f"轉換前的矩形頂角=\{box}")
points=cv2.boxPoints(box)
points=np.int32(points)
print(f"轉換後的矩形頂角=\n{points}")
dst=cv2.drawContours(src,[points],0,(0,255,0),2)

cv2.namedWindow("src",cv2.WINDOW_NORMAL)
cv2.namedWindow("dst",cv2.WINDOW_NORMAL)
cv2.imshow("src",src)
cv2.imshow("dst",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()