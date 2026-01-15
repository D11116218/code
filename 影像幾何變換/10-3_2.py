import cv2

#影像縮放

src=cv2.imread("t1.jpg")
cv2.imshow("p1",src)
dst=cv2.resize(src,None,fx=0.5,fy=1.1)#縮放，fx:水平縮放比例，fy:垂直縮放比例
cv2.imshow("p2",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
