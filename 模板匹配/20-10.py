import cv2

src=cv2.imread("3.jpg",cv2.IMREAD_COLOR)
cv2.imshow("src",src)
temp1=cv2.imread("c.jpg",cv2.IMREAD_COLOR)
cv2.imshow("temp1",temp1)

H,W=src.shape[:2]
h,w=temp1.shape[:2]
result=cv2.matchTemplate(src,temp1,cv2.TM_CCOEFF_NORMED)