import cv2 as cv

img = cv.imread('Photo/Face.jpg')
# cv.imshow('Face_Detect', img)


gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Face_Detect_Gray', gray)

haar_cascade = cv.CascadeClassifier('haar_face.xml')

faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 3, minSize = (5, 5))
# 參數(1) _ img：BGR 或 灰階皆可，灰階圖能降低 noise
# 參數(2) _ scaleFactor：每次搜尋方塊減少的比例

print(f'Number of faces found = {len(faces_rect)}')

for (x, y, w, h) in faces_rect:
	cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness = 2)

cv.imshow('Detected_Face', img)

cv.waitKey(0)