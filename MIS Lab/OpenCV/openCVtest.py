import cv2 as cv
import numpy as np

# 讀入圖片
img = cv.imread('Photo/MAMAMOO.jpg')


# 縮放大小
def rescaleFrame(frame, scale = 0.75):
	# 可用於 img、Video、live Video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


# 顯現圖片
cv.imshow('TestBig', img)

# 縮放圖片
resize_img = rescaleFrame(img)
cv.imshow('TestSmall', resize_img)

# 於圖片上繪製圖形
## 1. Draw a Rectangle
cv.rectangle(resize_img, (0,0), (resize_img.shape[1]//2, resize_img.shape[0]//2), (0, 255, 0), thickness=-1)
cv.imshow('Test_Rectangle', resize_img)

## 2. Draw a Circle
cv.circle(resize_img, (resize_img.shape[1]//2, resize_img.shape[0]//2), 40, (0, 0, 255), thickness = -1)
cv.imshow('Test_Circle', resize_img)

## 3. Draw a Line
cv.line(resize_img, (100, 250), (resize_img.shape[1]//2, resize_img.shape[0]//2), (255, 255, 255), thickness = 3)
cv.imshow('Test_Line', resize_img)

## 4. Write Text
cv.putText(resize_img, 'MAMAMOO', (255, 255), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0, 255, 0), thickness = 2)
cv.imshow('Test_Text', resize_img)


cv.waitKey(0)