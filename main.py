import cv2
import numpy as np
import os
cap = cv2.VideoCapture(0)
# Save video for debugging purposes
out = cv2.VideoWriter('ProgramControl.avi',-1, 5.0, (640,480))
handThreshold = 0
previousHand = 0
while( cap.isOpened() ) :
    # Save previous hand state
    previousHand = handThreshold
    # Read in webcam data
    ret,img = cap.read()
    # Create grayscale version for faster analysis
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Blur image to factor out any interference
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # Using built in OpenCV program to detect threshold of images
    # Values need to be adjusted depending upon lighting situation
    ret,thresh1 = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # Finally detect contours. Hierarchy wasn't needed for me, but may be of use for
    # further operations
    _, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Find needed spots to illustrate
    drawing = np.zeros(img.shape,np.uint8)

    max_area=0

    # Iterate through contours. Put some of the secret sauce here
    for i in range(len(contours)):
      cnt = contours[i]
      area = cv2.contourArea(cnt)
      if(area > max_area):
        max_area = area
        ci = i
    # Save the maximum contour
    maxCnt = contours[ci]
    # Now form "hull" around this area, beware that poor lighting can damage results
    hull = cv2.convexHull(maxCnt)
    # Now calculate the moments for analysis in next statement
    moments = cv2.moments(maxCnt)
    if moments['m00'] != 0:
      cx = int(moments['m10'] / moments['m00']) # Divsion being done is cx = M10/M00
      cy = int(moments['m01'] / moments['m00']) # Division being done is cy = M01/M00

    # Now drawing circle in the center of the detected main area; Used for debugging
    centr=(cx,cy)
    # Render this circle, increasing radius may help with viewing
    cv2.circle(img, centr, 5, [0,0,255],2)
    # Finally render all the components over the drawing computed by numpy
    cv2.drawContours(drawing,[maxCnt],0,(0,255,0),2)
    cv2.drawContours(drawing,[hull],0,(0,0,255),2)

    # Finish up all the needed computations before full digit processing
    cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    hull = cv2.convexHull(cnt,returnPoints = False)

    # Delineate section with possiblity to make block optional in future versions of program
    if(1):
       defects = cv2.convexityDefects(cnt,hull)
       mind=0
       maxd=0
       allFar = []
       # Prepare and detect everything for actual finger processing
       for i in range(defects.shape[0]):
         # Extract pertinent array values
         s, e, f, d = defects[i,0]
         start = tuple( cnt[s][0] )
         end = tuple( cnt[e][0] )
         far = tuple( cnt[f][0] )
         allFar.append( far )
         dist = cv2.pointPolygonTest(cnt,centr,True)
         cv2.line(img,start,end,[0,255,0],2)
         cv2.circle(img,far,5,[0,0,255],-1)
       print "Searching for hand..."
       # Finally! detect number of digits visible to detect if hand is raised
       for x in allFar:
         hitCount = 0
         # Detect width and form to see if fingers line up
         for b in allFar:
           if (x[1]-b[1])<20 and (x[1]-b[1])>-20:
             hitCount+=1
         # Check if hand detection is complete
         if hitCount>2:
           handThreshold+=1
           print "Hand Detected!"
           cv2.circle(drawing, x, 40, [255, 255, 255], -1)
         else:
           if handThreshold > 0:
             handThreshold-=1
       i=0

    # Render both images for analyis (will be removed in final product)
    cv2.imshow('output',drawing)
    cv2.imshow('input',img)
    out.write(drawing)

    k = cv2.waitKey(10)

    # Shut down the program if key pressed (change value to whatever key you want) 
    if k == 113:
        break
        out.release()

    # If hand has been held up for 10+ correctly identified frames, start program
    if handThreshold == 10 and previousHand < handThreshold:
        os.system("start C:/Users/noah/Desktop/anki.lnk")
