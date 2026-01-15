import cv2

#影像縮放

src=cv2.imread("t1.jpg")
cv2.imshow("p1",src)
width = 300
height=200
dsize=(width,height)
dst=cv2.resize(src,dsize)#縮放，dsize:輸出影像尺寸
cv2.imshow("p2",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
