import cv2
import matplotlib.pyplot as plt
#直方圖繪製
src=cv2.imread("t1.jpg",cv2.IMREAD_GRAYSCALE)
cv2.imshow("Src",src)
plt.hist(src.ravel(),256)#繪製直方圖
hist=cv2.calcHist([src],[0],None,[256],[0,256])#計算直方圖

print(f"資料類型={type(hist)}")
print(f"資料外觀={hist.shape}")
print(f"資料大小={hist.size}")
print(f"資料內容 \n{hist}")
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
