import cv2
import numpy as np
#2D濾波核
#可以自訂義卷積核(濾波核)
src=cv2.imread("t1.jpg")
kernel=np.ones((11,11),np.float32)/121  #自訂義卷積核
#建立11x11矩陣(像是模板)，每個元素 = 1/121
dst=cv2.filter2D(src,-1,kernel)         #自訂義濾波器
#-1 為自動匹配輸入型別
cv2.imshow("src",src)
cv2.imshow("kernel",dst)

cv2.waitKey()
cv2.destoryAllWindows()