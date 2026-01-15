import cv2

#影像旋轉

src=cv2.imread("t1.jpg")
cv2.imshow("A1",src)

height,width=src.shape[0:2]#例:(480, 640, 3)高、寬、三通道，索引0:2表示高、寬

M=cv2.getRotationMatrix2D((width/2,height/2),30,1)#旋轉30度、1不縮放
dsize=(width,height)
dst1=cv2.warpAffine(src,M,dsize)
cv2.imshow("A2",dst1)

M=cv2.getRotationMatrix2D((width/2,height/2),-30,1)#旋轉-30度、1不縮放
dst=cv2.warpAffine(src,M,dsize)#執行仿射
cv2.imshow("A3",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()