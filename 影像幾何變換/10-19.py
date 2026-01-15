import cv2
import numpy as np

src=np.random.randint(0,256,size=[3,4],dtype=np.uint8)#3列4行
rows,cols=src.shape#原圖像的行、列
mapx=np.zeros(src.shape,np.float32)#和原圖一樣大的矩陣，每個元素都設為0
mapy=np.zeros(src.shape,np.float32)#和原圖一樣大的矩陣，每個元素都設為0
for r in range(rows):
    for c in range(cols):

        #行:左到右，列:上到下

        mapx[r,c]=c#設mapx的第r行第c列設為c
        mapy[r,c]=r#設mapy的第r行第c列設為r

dst=cv2.remap(src,mapx,mapy,cv2.INTER_LINEAR)#雙線性插值法
#雙線性插值法:當映射座標為非整數時，用4個鄰近像素的加權平均計算

print(f"src=\n{src}")
print(f"mapx=\n{mapx}")
print(f"mapy=\n{mapy}")
print(f"dst=\n{dst}")