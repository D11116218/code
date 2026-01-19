import cv2

src=cv2.imread("c.jpg",cv2.IMREAD_COLOR)
cv2.imshow(src)
H,W=src.shape[:2]
print(f"原始影像高H={H},寬W={W}")
temp1=cv2.imread("a.jpg",cv2.IMREAD_COLOR)
cv2.imshow(temp1)
h,w=src.shape[:2]
print(f"原始影像高w={h},寬w={w}")
result=cv2.matchTemplate(src,temp1,cv2.TM_SQDIFF) #平方差匹配法
print(f"result大小={result.shape}")
print(f"陣列內容\n {result}")