import cv2

src=cv2.imread("e.jpg",cv2.IMREAD_GRAYSCALE)
dst=cv2.Laplacian(src,cv2.CV_16F,ksize=1)
dst1=cv2.convertScaleAbs(dst)

dst=cv2.Laplacian(src,cv2.CV_16F,ksize=3)
dst2=cv2.convertScaleAbs(dst)

dst=cv2.Laplacian(src,cv2.CV_16F,ksize=5)
dst3=cv2.convertScaleAbs(dst)

cv2.namedWindow("src",cv2.WINDOW_NORMAL)
cv2.namedWindow("dst1",cv2.WINDOW_NORMAL)
cv2.namedWindow("dst2",cv2.WINDOW_NORMAL)
cv2.namedWindow("dst3",cv2.WINDOW_NORMAL)

cv2.imshow("src",src)
cv2.imshow("dst1",dst1)
cv2.imshow("dst2",dst2)
cv2.imshow("dst3",dst3)

cv2.waitKey(0)
cv2.destroyAllWindows()
