import cv2

#單模板匹配

src=cv2.imread("3.jpg",cv2.IMREAD_COLOR)
cv2.imshow("src",src)
temp1=cv2.imread("c.jpg",cv2.IMREAD_COLOR)
h,w=temp1.shape[:2]
result=cv2.matchTemplate(src,temp1,cv2.TM_SQDIFF_NORMED)#單模板匹配
minval,maxval,minloc,maxloc=cv2.minMaxLoc(result)
#陣列中的 最小值,最大值,最小值座標,最大值座標

upperleft=minloc                                       #左上角座標
lowweright=(minloc[0]+w,minloc[1]+h)                   #右下角座標
dst=cv2.rectangle(src,upperleft,lowweright,(0,0,255),2)
print(f"result大小={result}")
print(f"陣列內容 \n{result}")
cv2.waitKey()
cv2.destroyAllWindows()