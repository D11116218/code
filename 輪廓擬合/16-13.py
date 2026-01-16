import cv2
import numpy as np
#擬合直線
src=cv2.imread("c.jpg")
src_gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
ret,dst_binary=cv2.threshold(src_gray,175,255,cv2.THRESH_BINARY)
contours,hierarchy=cv2.findContours(dst_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

#取得圖片尺寸
rows,cols=src.shape[:2]

#擬合直線
vx,vy,x,y=cv2.fitLine(contours[0],cv2.DIST_L2,0,0.01,0.01)
#針對第一個物體的輪廓點、距離類型(L2)、距離參數、半徑、角度
print(f"共線正規化向量={vx},{vy}")
print(f"直線經過的點={x},{y}")
#計算公式
lefty=int((-x*vy/vx)+y)
righty=int(((cols-x)*vy/vx)+y)

dst=cv2.line(src,(0,lefty),(cols-1,righty),(0,255,0),2)
#直線起點、直線終點、綠色、粗細

cv2.namedWindow("dst",cv2.WINDOW_NORMAL)
cv2.imshow("dst",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()