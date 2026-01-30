import cv2

#多目標匹配

src=cv2.imread("12.jpg",cv2.IMREAD_COLOR)
cv2.imshow("src",src)
temp1=cv2.imread("121.jpg",cv2.IMREAD_COLOR)
cv2.imshow("temp1",temp1)

h,w=temp1.shape[:2]
result=cv2.matchTemplate(src,temp1,cv2.TM_CCOEFF_NORMED)#模板匹配

#片歷所有陣列找出相似度大於0.95陣列
for row in range(len(result)):
    for col in range(len(result[row])):
        if result[row] [col]>0.95:
            dst=cv2.rectangle(src,(col,row),(col+w ,row+h),(0,255,0),3)

cv2.namedWindow("dst",cv2.WINDOW_NORMAL)

cv2.imshow("dst",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()