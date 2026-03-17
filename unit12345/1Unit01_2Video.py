#1Unit01_2Video.py
import cv2

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    cv2.imshow('Unit01_2 | StudentID | ', image)
    if cv2.waitKey(1) & 0xFF == 27:
       break
cap.release()
cv2.destroyAllWindows()
