#1Unit01_1pic.py
import cv2

cap = cv2.VideoCapture('pic/cat_and_dog.jpg')
success, img = cap.read()
cv2.imshow('Unit01_1 | StudentID | ', img)
cv2.waitKey(0)