import cv2
import numpy as np
import pyautogui

SCREEN_SIZE = tuple(pyautogui.size())


video= cv2.VideoCapture(0)

width= int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer= cv2.VideoWriter('basicvideo.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
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
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
while True:
    img = pyautogui.screenshot()
    img = np.array(img)
    ret,frame= video.read()
    success, img = video.read()
    writer.write(frame)
    imgResult = img.copy()
    findColor(img,myColors)
    cv2.imshow('frame', imgResult)
    output = cv2.bitwise_and(frame,frame,imgResult)

    if cv2.waitKey(1) & 0xFF == 27:
        break


video.release()
writer.release()
cv2.destroyAllWindows()
