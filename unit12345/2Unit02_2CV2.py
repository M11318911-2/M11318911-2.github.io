#2Unit02_2CV2.py
import cv2
import numpy as np

img=cv2.imread("pic/cat_and_dog.jpg")
img= cv2.resize(img, (320,200))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)
imgCanny = cv2.Canny(img, 300,300)
imghor = np.hstack((imgGray,imgBlur,imgCanny))
imgver = np.vstack((imghor,imghor))
cv2.imshow("Unit02_2 | StudentID |", imgver)
cv2.waitKey(0)
