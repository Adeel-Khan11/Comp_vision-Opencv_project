import cv2
import mediapipe as mp
import time
import Handtrackingmodule as htm

pastTime=0
currentTime=0
cap=cv2.VideoCapture(0)
detector=htm.handDetector()
    


while True:
     success,image=cap.read()
     image=detector.handsfind(image,draw=False)
     ldlist=detector.findpos(image,draw=False)
     if len(ldlist) !=0:
         print(ldlist[4])
     currentTime=time.time()
     fps=1/(currentTime-pastTime)
     pastTime=currentTime
    
     cv2.putText(image,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    
    
     cv2.imshow('image',image)
    # Exit loop when ESC is pressed
     if cv2.waitKey(1) & 0xFF == 27:
        break