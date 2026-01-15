import cv2

src=cv2.imread("e.jpg",cv2.IMREAD_GRAYSCALE)
dst=cv2.GaussianBlur(src,(5,5),0)
dstx=cv2.Sobel(src,cv2.CV_32F,1,0)
dsty=cv2.Sobel(src,cv2.CV_32F,0,1)
dstx=cv2.convertScaleAbs(dstx)
dsty=cv2.convertScaleAbs(dsty)
dst_Sobel=cv2.addWeighted(dstx,0.5,dsty,0.5,0)


dstx=cv2.Scharr(src,cv2.CV_32F,1,0)
dsty=cv2.Scharr(src,cv2.CV_32F,0,1)
dstx=cv2.convertScaleAbs(dstx)
dsty=cv2.convertScaleAbs(dsty)#絕對值
dst_Scharr=cv2.addWeighted(dstx, 0.5,dsty, 0.5, 0)

dst_tmp=cv2.Laplacian(src,cv2.CV_32F,ksize=3)
dst_lap=cv2.convertScaleAbs(dst_tmp)
dst_canny=cv2.Canny(src,50,100)

cv2.namedWindow("dst_Sobel",cv2.WINDOW_NORMAL)
cv2.namedWindow("dst_Scharr",cv2.WINDOW_NORMAL)
cv2.namedWindow("dst_tmp",cv2.WINDOW_NORMAL)
cv2.namedWindow("dst_canny",cv2.WINDOW_NORMAL)

cv2.imshow("dst_Sobel",dst_Sobel)
cv2.imshow("dst_Scharr",dst_Scharr)
cv2.imshow("dst_tmp",dst_lap)
cv2.imshow("dst_canny",dst_canny)
cv2.waitKey()
cv2.destroyAllWindows()