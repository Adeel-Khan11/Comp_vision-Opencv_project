import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,1,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    
    def handsfind(self,image,draw=True):


        imgRGB=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
          for handlms in self.results.multi_hand_landmarks:
             if draw:
            
              self.mpDraw.draw_landmarks(image,handlms,self.mpHands.HAND_CONNECTIONS)
        return image
    
    
    def findpos(self,image,handno=0,draw=True):
        ldlist=[]
            
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handno]
            for id,lm in enumerate(myhand.landmark):
                # print(id,lm)
                h,w,c=image.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                # print(id,cx,cy)
                ldlist.append([id,cx,cy])
                
                if draw:
                    cv2.circle(image,(cx,cy),5,(255,0,255),cv2.FILLED)
        return ldlist
        

  
    
cv2.destroyAllWindows()


def main():
    pastTime=0
    currentTime=0
    cap=cv2.VideoCapture(0)
    detector=handDetector()
    


    while True:
     success,image=cap.read()
     image=detector.handsfind(image)
     ldlist=detector.findpos(image)
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
    


if __name__=='__main__':
    main()