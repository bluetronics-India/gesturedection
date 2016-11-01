import numpy as np
import cv2

cap = cv2.VideoCapture(0)

iterations = 0
scope = [[0, 0, 0], [0, 0, 0]]

while(True):
    ret, frame = cap.read()
    topSize = len(frame)/4
    lowerSize = len(frame[len(frame)/4])/4
    dot = (lowerSize*2, topSize*2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if iterations < 40:
      cv2.putText(frame, 'Prepping...', (lowerSize*2, topSize*2),font,2,(255, 255, 255), 2)
    if iterations == 40:
        scope[0][0] = frame[topSize*2][lowerSize*2][0]
        scope[1][0] = frame[topSize*2][lowerSize*2][0]
        scope[0][1] = frame[topSize*2][lowerSize*2][1]
        scope[1][1] = frame[topSize*2][lowerSize*2][1]
        scope[0][2] = frame[topSize*2][lowerSize*2][2]
        scope[1][2] = frame[topSize*2][lowerSize*2][2]
    if iterations > 40 and iterations < 100:
      if scope[0][0] > frame[topSize*2][lowerSize*2][0]:
        scope[0][0] = frame[topSize*2][lowerSize*2][0]
      elif scope[1][0] < frame[topSize*2][lowerSize*2][0]:
        scope[1][0] = frame[topSize*2][lowerSize*2][0]
      if scope[0][1] > frame[topSize*2][lowerSize*2][1]:
        scope[0][1] = frame[topSize*2][lowerSize*2][1]
      elif scope[1][1] < frame[topSize*2][lowerSize*2][1]:
        scope[1][1] = frame[topSize*2][lowerSize*2][1]
      if scope[0][2] > frame[topSize*2][lowerSize*2][2]:
        scope[0][2] = frame[topSize*2][lowerSize*2][2]
      elif scope[1][2] < frame[topSize*2][lowerSize*2][2]:
        scope[1][2] = frame[topSize*2][lowerSize*2][2]
    if iterations == 100:
      scope[0][0]-=10
      scope[0][1]-=10
      scope[0][2]-=10
      scope[1][0]+=10
      scope[1][1]+=10
      scope[1][2]+=10

    dotScope = 0
    if iterations > 100:
      dot = (0, 0)
      for i in range(topSize):
        for a in range(lowerSize):
          first = frame[i*4][a*4][0]
          second = frame[i*4][a*4][1]
          third = frame[i*4][a*4][2]
          par = 0
          if first >= scope[0][0] and first <= scope[1][0]:
            par += 1
          if second >= scope[0][1] and second <= scope[1][1]:
            par += 1
          if third >= scope[0][2] and third <= scope[1][2]:
            par += 1
          if par > 2:
            if dotScope == 0:
              dotScope = [[a*4, i*4], [a*4, i*4]]
            else:
              if dotScope[0][0] > a*4:
                dotScope[0][0] = a*4
              elif dotScope[1][0] < a*4:
                dotScope[1][0] = a*4
              if dotScope[0][1] > i*4:
                dotScope[0][1] = i*4
              elif dotScope[1][1] < i*4:
                dotScope[1][1] = i*4
        if not dotScope == 0:
          print dotScope
          dot = (((dotScope[1][0]-dotScope[0][0])/2)+dotScope[0][0],
                  ((dotScope[1][1]-dotScope[0][1])/2)+dotScope[0][1])
    cv2.circle(frame,dot, 10, (0, 255, 0), -5)
    cv2.imshow('img',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    iterations += 1
    '''
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #newgray = np.array(gray, dtype='uint8')
    '''

'''
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.circle(frame,(x + (w / 2), y + ( 4 * (h / 5))), 10, (0, 255, 0), -5)
        #frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = frame[y:y+h, x:x+w]
        #eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes:
           # cv2.line(roi_color,(ex + (ew/2), ey),(ex +(ew / 2), ey + eh),(0, 0, 255))
           # cv2.line(roi_color,(ex, ey + (eh / 2)), (ex + ew, ey + (eh / 2)), (0, 0, 255))
           # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

'''

cv2.destroyAllWindows()
