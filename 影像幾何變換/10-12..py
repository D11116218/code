import cv2
import numpy as np

#影像傾斜

src=cv2.imread("t1.jpg")
cv2.imshow("A1",src)

height,width=src.shape[0:2]
srop=np.float32([[0,0],[width-1,0],[0,height-1]])
dstp=np.float32([[30,0],[width-1,0],[0,height-1]])
M=cv2.getAffineTransform(srop,dstp)
dsize=(width,height)
dst=cv2.warpAffine(src,M,dsize)
cv2.imshow("A2",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()