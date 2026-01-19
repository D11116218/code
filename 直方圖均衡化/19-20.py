import cv2
#自適應直方圖均衡化
src=cv2.imread("t1.jpg",cv2.IMREAD_GRAYSCALE)
cv2.imshow("src",src)
clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))#建立自適應直方圖均衡化
dst=clahe.apply(src)#應用自適應直方圖均衡化
cv2.imshow("dst",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()