import cv2
import numpy as np

src=cv2.imread("t1.jpg")
dst=cv2.Sobel(src,-1,1,0)
#邊緣檢測(自動調適適合的影像深度，x方向，y方向)
dst=cv2.convertScaleAbs(dst)#將負值轉正值(取絕對值)，範圍調整到0~255、轉換型別unit8
cv2.imshow("src",src)
cv2.imshow("dst",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()

#目標影像深度(型別)
#自動調適影像深度 -1
# CV_8U = 0：8位元無符號整數
# CV_16U = 2：16位元無符號整數
# CV_16S = 3：16位元有符號整數
# CV_32F = 5：32位元浮點數
# CV_64F = 6：64位元浮點數