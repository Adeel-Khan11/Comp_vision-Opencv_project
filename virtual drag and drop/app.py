import cv2
from module.Handtrackingmodule import handDetector
import cvzone
import numpy as np

class drawRect():
    def __init__(self, poscenter,size=[100,100]):
        self.poscenter = poscenter
        self.size = size
    
    def update(self,cursor):
        cx,cy=self.poscenter
        w,h=self.size
        
        fx,fy=int(cursor[1]),int(cursor[2])
        
        if cx-w//2 < fx < cx+w//2 and cy-h//2 < fy < cy+h//2:
            self.poscenter=[fx,fy]


    def contains(self, cursor):
        fx,fy = int(cursor[1]), int(cursor[2])
        cx,cy = self.poscenter
        w,h = self.size
        return (cx - w//2 < fx < cx + w//2) and (cy - h//2 < fy < cy + h//2)
 

rect=drawRect([150,150])

cap=cv2.VideoCapture(1)
cap.set(3,920)
cap.set(4,920)
detector=handDetector(detectionCon=0.8)

cx,cy,w,h=200,200,200,200

reclist=[]
for x in range(5):
    reclist.append(drawRect([x*150+150,150]))


colors = [
    (255, 0, 255),
    (0, 255, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 128, 0),
]

while True:
    
    success,image=cap.read()
    image=cv2.flip(image,1)
    image=detector.handsfind(image)
    lmlist=detector.findpos(image)
    colorRec=(255,0,255)
    if lmlist:
        
        l,_,_=detector.findDistance(8,12,image,draw=False)
        # print(l)
        if l<30:
            cursor=lmlist[8]

            for rect in reclist:
                if rect.contains(cursor):
                    rect.update(cursor)
                    break
      
    # If you prefer **solid** rectangles (no transparency), uncomment this block and
    # comment out the per-rectangle blending block below.
    
    # for i, rect in enumerate(reclist):
    #     cx, cy = rect.poscenter
    #     w, h = rect.size
    #     fill_color = colors[i % len(colors)]
    #     # draw solid filled rectangle directly on the frame
    #     cv2.rectangle(image, (cx - w // 2, cy - h // 2),
    #                   (cx + w // 2, cy + h // 2), fill_color, cv2.FILLED)
    #     # optional: draw corner decoration (cvzone)
    #     cvzone.cornerRect(image, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)
    #
  

    # Per-rectangle ROI blending (prevents merged blob)
    out = image.copy()
    alpha = 0.5

    for i, rect in enumerate(reclist):
        cx, cy = rect.poscenter
        w, h = rect.size

        
        x1 = max(0, cx - w // 2)
        y1 = max(0, cy - h // 2)
        x2 = min(out.shape[1], cx + w // 2)
        y2 = min(out.shape[0], cy + h // 2)

      
        if x2 <= x1 or y2 <= y1:
            continue

        rw = x2 - x1
        rh = y2 - y1

        fill_color = colors[i % len(colors)]

        
        tmp_roi = np.zeros((rh, rw, 3), dtype=np.uint8)
        cv2.rectangle(tmp_roi, (0, 0), (rw, rh), fill_color, cv2.FILLED)

        
        blended = cv2.addWeighted(out[y1:y2, x1:x2], alpha, tmp_roi, 1 - alpha, 0)
        out[y1:y2, x1:x2] = blended

        
        cvzone.cornerRect(out, (x1, y1, rw, rh), 20, rt=0)
        cv2.rectangle(out, (x1, y1), (x2, y2), (0,0,0), 2)

  

    cv2.imshow("Image", out)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
