# import the necessary packages
from imutils.video import VideoStream
import argparse
import cv2
import imutils
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())
# load the video
if not args.get("video", False):
	camera = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
# keep looping
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

myColors = [0,86,170,80,255,255]

def findColor(img,myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(myColors[0:3])
    upper = np.array(myColors[3:6])
    mask = cv2.inRange(imgHSV,lower,upper)
    getContours(mask)
    #cv2.imshow("img",mask)
    
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
	# grab the current frame and initialize the status text
	frame = camera.read()
	status = "No Targets"
	# check to see if we have reached the end of the
	# video
	# convert the frame to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(gray,(0,86,170), (80,255,255))
	
	# find contours in the edge map
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
    # loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.01 * peri, True)
		# ensure that the approximated contour is "roughly" rectangular
		if len(approx) >= 4 and len(approx) <= 6:
			# compute the bounding box of the approximated contour and
			# use the bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			aspectRatio = w / float(h)
			# compute the solidity of the original contour
			area = cv2.contourArea(c)
			hullArea = cv2.contourArea(cv2.convexHull(c))
			solidity = area / float(hullArea)
			# compute whether or not the width and height, solidity, and
			# aspect ratio of the contour falls within appropriate bounds
			keepDims = w > 25 and h > 25
			keepSolidity = solidity > 0.9
			keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2
			# ensure that the contour passes all our tests
			if keepDims and keepSolidity and keepAspectRatio:
				# draw an outline around the target and update the status
				# text
				cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
				status = "Target(s) Acquired"
				# compute the center of the contour region and draw the
				# crosshairs
				M = cv2.moments(approx)
				(cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
				(startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
				(startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
				cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
				cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)
                # draw the status text on the frame
	cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
		(0, 0, 255), 2)
	# show the frame and record if a key is pressed
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
while True:
 
    success, img = cap.read()
    imgResult = img.copy()
    findColor(img, myColors)
    cv2.imshow('Hasil', imgResult)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
 
cap.release()
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()