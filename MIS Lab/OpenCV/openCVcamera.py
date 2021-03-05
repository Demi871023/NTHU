import cv2 as cv

cap = cv.VideoCapture(0)

# 確認攝影機是否有開啟
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 導入分類器
haar_cascade = cv.CascadeClassifier('haar_face.xml')

while(True):
    # 以 frame 形式讀取相機裡面的影像
    ret, frame = cap.read()

    # 如果有讀取到影像，ret 就會是 true
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 3)
    # 參數(3) _ minNeighbors：每個目標至少檢測到幾次以上，才可被認定是真數據

    for (x, y, w, h) in faces_rect:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness = 2)
    # 顯示圖片
    cv.imshow('frame', frame)
    # 按下 q 鍵離開迴圈
    if cv.waitKey(1) == ord('q'):
        break

# 釋放該攝影機裝置
cap.release()
cv.destroyAllWindows()