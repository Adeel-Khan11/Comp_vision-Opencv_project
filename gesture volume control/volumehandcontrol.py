########################################################
import sys
import cv2
import numpy as np
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from module import Handtrackingmodule as htm 

#########################################################

sys.path.append(r"D:\computer vision project\hand-tracking-30fps")
detector = htm.handDetector(detectionCon=0.8)
wCam, hCam = 640, 480
cap = cv2.VideoCapture(1)  
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  wCam)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)  


################################################################

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_vol, max_vol, step = volume.GetVolumeRange()
print(f"Volume range: {min_vol} dB to {max_vol} dB, step {step} dB")

##################################################################
volbar=400
ptime = 0.0
volper=0
while True:
    success, image = cap.read()
    if not success:
        continue

    image = detector.handsfind(image)
    lmlist = detector.findpos(image, draw=False)
    if len(lmlist) > 8: 
      
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        
        accent_color = (0, 255, 0)  # neon green
        
        cv2.circle(image, (x1, y1), 7, accent_color, cv2.FILLED)
        cv2.circle(image, (x2, y2), 7, accent_color, cv2.FILLED)
        cv2.line(image,(x1,y1),(x2,y2),accent_color,3)
        cv2.circle(image, (cx, cy), 7, accent_color, cv2.FILLED)
        
        length=math.hypot(x2-x1,y2-y1)
        
        # Map hand distance to scalar volume (0.0 to 1.0)
        vol_scalar = float(np.interp(length, [23, 200], [0.0, 1.0]))
        vol_scalar = max(0.0, min(1.0, vol_scalar))  # Clamp between 0.0 and 1.0

        # Set system volume using scalar
        volume.SetMasterVolumeLevelScalar(vol_scalar, None)

# UI values for bar and percentage
        volbar = np.interp(vol_scalar, [0.0, 1.0], [400, 150])
        volper = vol_scalar * 100.0

        
        if length < 23:
            cv2.circle(image, (cx, cy), 7, (0, 0, 255), cv2.FILLED)  # red when close
    
    # Volume bar
    cv2.rectangle(image,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(image,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)
    
    # Volume % text in bright yellow
    cv2.putText(image, f'{int(volper)} %', (40, 450),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
            
    # FPS in bright yellow
    ctime = time.time()
    fps = 1.0 / max(1e-6, (ctime - ptime))
    ptime = ctime

    cv2.putText(image, f'FPS: {int(fps)}', (40, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow('image', image)
    if cv2.waitKey(1) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()
