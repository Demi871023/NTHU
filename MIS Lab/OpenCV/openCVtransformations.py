import cv2 as cv
import numpy as np

img = cv.imread('Photo/MAMAMOO.jpg')

cv.imshow('MAMAMOO', img)

# Translate
def translate(img, x, y):
	transMat = np.float32([[1, 0, x], [0, 1, y]])
	dimensions = (img.shape[1], img.shape[0])
	return cv.warpAffine(img, transMat, dimensions)

# -x ----> left
# -y ----> up
# x  ----> right
# y  ----> down

translated = translate(img, 100, 100)
cv.imshow('TestTranslated', translated)

# Rotate
def rotate(img, angle, rotPoint=None):
	(height, width) = img.shape[:2]

	if rotPoint is None:
		rotPoint = (width//2, height//2)

	rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
	dimensions = (width, height)

	return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(img, 45)
cv.imshow('TestRotated', rotated)

# Flipping
flip = cv.flip(img, -1)
cv.imshow('TestFlip', flip)


cv.waitKey(0)