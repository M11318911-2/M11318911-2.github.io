#2Unit02_5CV5.py
import cv2
from time import strftime
import os
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, frame = cap.read()
    cv2.imshow('Unit02_5 | StudentID |', frame)
    keyb = cv2.waitKey(100) & 0xFF
    if keyb == 27:
        break
    elif keyb == ord('0'):
        systime = strftime("%H%M%S")
        imgname = os.path.join('pic/', systime + '.jpg')
        cv2.imwrite(imgname, frame)
        print(imgname)
cap.release()
cv2.destroyAllWindows()
