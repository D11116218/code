import cv2
import numpy as np

src=cv2.imread("c.jpg")
cv2.namedWindow("src",cv2.WINDOW_NORMAL)
cv2.imshow("src",src)
src_gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
ret,dst_binary=cv2.threshold(src_gray,127,255,cv2.THRESH_BINARY)
contours,hierarchy=cv2.findContours(dst_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


box=cv2.minAreaRect(contours[1])
#可旋轉貼合物件的最小矩形
#cv2.boundingRect(CONTOURS[0])，貼齊(水平/垂直)的矩形
print(f"轉換前的矩形頂角={box}")
points=cv2.boxPoints(box)#取頂點座標
points=np.int32(points)
print(f"轉換後的矩形頂角=\n{points}")
dst=cv2.drawContours(src,[points],0,(0,255,0),2)#畫輪廓

cv2.namedWindow("dst",cv2.WINDOW_NORMAL)
cv2.imshow("dst",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()