import cv2

#影像翻轉

src=cv2.imread("t1.jpg")
cv2.imshow("src",src)
dst1=cv2.flip(src,0)#垂直
cv2.imshow("dst1-flip vertically",dst1)
dst2=cv2.flip(src,1)#水平
cv2.imshow("dst2-flip horizontally",dst2)
dst3=cv2.flip(src,-1)#垂直和水平
cv2.imshow("dst3-flip vertically and horizontally",dst3)

cv2.waitKey(0)
cv2.destroyAllWindows()
