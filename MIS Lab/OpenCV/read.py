import cv2 as cv
import numpy as np

img = cv.imread('Photo/MAMAMOO.jpg')

def rescaleFrame(frame, scale = 0.2):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

resize_img = rescaleFrame(img)

cv.imshow('Test', resize_img)
cv.waitKey(0)