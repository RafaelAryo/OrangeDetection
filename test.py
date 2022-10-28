import cv2
import numpy as np

from virtualpain import getContours

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_output = cv2.VideoWriter('HASIL.avi' , fourcc, 60, (640,480))
myColors = [0,163,80,24,255,255]

def findColor(img,myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(myColors[0:3])
    upper = np.array(myColors[3:6])
    mask = cv2.inRange(imgHSV,lower,upper)
    getContours(mask)
    cv2.imshow("img",mask)

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(imgResult, cnt, -1. (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)

while (True):
    ret, frame = cap.read()
    success, img = cap.read()
    imgResult = img.copy()
    findColor(img, myColors)
    cv2.imshow('Hasil', imgResult)
    output = cv2.bitwise_and(frame,frame)

    if cv2.waitKey(1) and 0xFF == ord('a'):
        break

cap.release()
video_output.release()
cv2.destroyAllWindows()