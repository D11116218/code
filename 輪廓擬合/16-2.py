import cv2
#矩形_貼齊(水平/垂直)的矩形
src=cv2.imread("c.jpg",cv2.IMREAD_GRAYSCALE)
#二值化
ret,dst_binary=cv2.threshold(src,127,255,cv2.THRESH_BINARY)
#閾值，大於127設為255(設最大值)，小於則為0
#THRESH_BINARY二值化規則規則
CONTOURS,hierarchy=cv2.findContours(dst_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#二值化圖像、列出所有輪廓、儲存物件輪廓線的起點和終點
#CHAIN_APPROX_none:儲存物件輪廓線上每個點
#CONTOURS:儲存數據
rect=cv2.boundingRect(CONTOURS[0])
#CONTOURS[0]:抓取第一個物體
#定位物件四個位置極限值
print(f"元組 rect={rect}")

x,y,w,h=cv2.boundingRect(CONTOURS[0])

dst=cv2.rectangle(src,(x,y),(x+w,y+h),(0,255),2)
cv2.namedWindow(dst,cv2.WINDOW_NORMAL)
cv2.imshow("dst",dst)
print(f"左上角 x={x} ,y={y}")
print(f"矩形寬度   ={w}")
print(f"矩形高度   ={h}")
cv2.waitKey(0)
cv2.destroyAllWindows()