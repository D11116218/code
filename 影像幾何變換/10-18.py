import cv2
import numpy as np

#影像重映射

src=np.random.randint(0,256,size=[3,4],dtype=np.uint8)#3x4隨機數字圖像陣列
rows,cols=src.shape#取得原圖像尺寸
mapx=np.ones(src.shape,np.float32)*3#和原圖一樣大的矩陣，每個元素都設為3
mapy=np.ones(src.shape,np.float32)*2#和原圖一樣大的矩陣，每個元素都設為2

dst=cv2.remap(src,mapx,mapy,cv2.INTER_LINEAR)#原圖、mapx行、mapy列、雙線性插值法

#雙線性插值法：在原圖像中，每個像素點的值是由其周圍4個像素點的值加權平均得到的。

print("src=\n",src)
print("mapx=\n",mapx)
print("mapy=\n",mapy)
print("dst=\n",dst)