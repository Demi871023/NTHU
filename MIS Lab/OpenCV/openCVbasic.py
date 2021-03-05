import cv2 as cv
import numpy as np

# 讀入圖片
img = cv.imread('Photo/MAMAMOO.jpg')


# 顯現圖片
cv.imshow('TestBig', img)

# Converting to grayscale 將 BGR 圖片轉成 Gray 圖片
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('TestGray', gray)

# Blur 模糊
blur = cv.GaussianBlur(img, (7, 7), cv.BORDER_DEFAULT)
cv.imshow('TestBlur', blur)

# Edge Cascade
canny = cv.Canny(blur, 125, 175)
cv.imshow('TestCanny', canny)

# Dilating the image 膨脹
dilated = cv.dilate(canny, (3,3), iterations = 3)
cv.imshow('TestDilated', dilated)

# Eroding 侵蝕
eroded = cv.erode(dilated, (3,3), iterations = 3)
cv.imshow('TestEroded', eroded)

# Resize
resized = cv.resize(img, (500, 500))
cv.imshow('TestResized', resized)

# Cropping 切割座標點圍起來的範圍圖像
cropped = img[50:200, 200:400]
cv.imshow('TestCropped', cropped)


cv.waitKey(0)