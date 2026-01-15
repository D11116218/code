import cv2
#Laplacian
src=cv2.imread("t1.jpg")
dst_tmp=cv2.Laplacian(src,cv2.CV_32F)#計算影像梯度
dst=cv2.convertScaleAbs(dst_tmp)#取絕對值，資料格式轉換uint8
cv2.imshow("src",src)
cv2.imshow("dst",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
