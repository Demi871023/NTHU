import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


img = cv.imread('Photo/Face.jpg')
# cv.imshow('MAMAMOO', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)
gray_hist = cv.calcHist([gray], [0], None, [256], [0, 256])

plt.figure()
plt.plot(gray_hist)
plt.show()


cv.waitKey(0)