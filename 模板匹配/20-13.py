import cv2

#多目標模板匹配

def myMatch(image,tmp):
    h,w=tmp.shape[0:2]
    result=cv2.matchTemplate(image,tmp,cv2.TM_CCOEFF_NORMED)
    for row in range(len(result)):
        for col in range(len(result[row])):
            if result[row] [col]>0.95:
                match.append([(col,row),(col+w,row+h)])
    return

src=cv2.imread("12.jpg",cv2.IMREAD_COLOR)
temps=[]
temp1=cv2.imread("121.jpg",cv2.IMREAD_COLOR)
temps.append(temp1)#加入匹配串列
temp2=cv2.imread("122.jpg",cv2.IMREAD_COLOR)
temps.append(temp2)
match=[]
for t in temps:#遍歷每個模板圖像
    myMatch(src,t)
for img in match:#遍歷所有匹配結果
    dst=cv2.rectangle(src,(img[0]),(img[1]),(0,255,0),3)
cv2.namedWindow("final",cv2.WINDOW_NORMAL)
cv2.imshow("final",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()