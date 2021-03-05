import cv2 as cv
import numpy as np

img = cv.imread('Photo/MAMAMOO.jpg')
cv.imshow('Face', img)

blank = np.zeros(img.shape[:2], dtype='uint8')

b, g, r = cv.split(img)

blue = cv.merge([b, blank, blank])
green = cv.merge([blank, g, blank])
red = cv.merge([blank, blank, r])

cv.imshow('Blue', b)
cv.imshow('Green', g)
cv.imshow('Red', r)

cv.imshow('BlueB', blue)
cv.imshow('BlueG', green)
cv.imshow('BlueR', red)

print(img.shape)
print(b.shape)
print(g.shape)
print(r.shape)


merged = cv.merge([b, g, r])
cv.imshow('Merge', merged)

cv.waitKey(0)