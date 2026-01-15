import cv2
import numpy as np

src=cv2.imread("t1.jpg")
rows,cols=src.shape[0:2]
mapx=np.zeros(src.shape[:2],np.float32)
mapy=np.zeros(src.shape[:2],np.float32)
for r in range(rows):
    for c in range(cols):
        if 0.25*rows<r<0.75*rows and 0.25*cols<c<0.75*cols:
            #當目標像素在原圖像的中心區域時才進行處理
            mapx[r,c] = 2*(c-0.25*cols)#水平放大2倍
            mapy[r,c] = 2*(r-0.25*rows)#垂直放大2倍
        else:#否則都不變
            mapx[r,c] = 0
            mapy[r,c] = 0
dst=cv2.remap(src,mapx,mapy,cv2.INTER_LINEAR)
cv2.imshow("src",src)
cv2.imshow("dst",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()