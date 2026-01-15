import cv2
#影像梯度
#特徵提取:找出物體輪廓、線條、邊界
#梯度=變化率
src=cv2.imread("t1.jpg")
#計算影像梯度
dstx=cv2.Sobel(src,cv2.CV_32F,1,0)
dsty=cv2.Sobel(src,cv2.CV_32F,0,1)
#負值轉正值
dstx=cv2.convertScaleAbs(dstx)
dsty=cv2.convertScaleAbs(dsty)
#融合
dst=cv2.addWeighted(dstx,0.5,dsty,0.5,0)

src=cv2.namedWindow("src", cv2.WINDOW_NORMAL)
dst=cv2.namedWindow("dst", cv2.WINDOW_NORMAL)

cv2.imshow("src",src)
cv2.imshow("dst",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()