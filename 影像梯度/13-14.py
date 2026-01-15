import cv2

src=cv2.imread("cc.jpg")
dstx=cv2.Sobel(src,cv2.CV_32F,1,0)
dsty=cv2.Sobel(src,cv2.CV_32F,0,1)
dstx=cv2.convertScaleAbs(dstx)
dsty=cv2.convertScaleAbs(dsty)
dst_Sobel=cv2.addWeighted(dstx,0.5,dsty,0.5,0)

dstx=cv2.Scharr(src,cv2.CV_32F,1,0)
dsty=cv2.Scharr(src,cv2.CV_32F,0,1)
dstx=cv2.convertScaleAbs(dstx)
dsty=cv2.convertScaleAbs(dsty)
dst_Sobel2=cv2.addWeighted(dstx,0.5,dsty,0.5,0)

cv2.namedWindow("src",cv2.WINDOW_NORMAL)
cv2.namedWindow("dstx",cv2.WINDOW_NORMAL)
cv2.namedWindow("dsty",cv2.WINDOW_NORMAL)
cv2.namedWindow("dst_Sobel",cv2.WINDOW_NORMAL)
cv2.namedWindow("dst_Sobel2",cv2.WINDOW_NORMAL)

cv2.imshow("src",src)
cv2.imshow("dstx",dstx)
cv2.imshow("dsty",dsty)
cv2.imshow("dst_Sobel",dst_Sobel)
cv2.imshow("dst_Sobel2",dst_Sobel2)

cv2.waitKey(0)
cv2.destroyAllWindows()