import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui as py


#########################
wcam,hcam=1024,768
ptime=0
wscr,hscr=py.size()
frameR=100 # frame reduction
seconds=2
smoothing=7
plocx,plocy=0,0
clocx,clocy=0,0
######################
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
detector=htm.handDetector(maxHands=1)
# print(wscr,hscr)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #1. find the hands landmarks
    img=detector.findhands(img)
    lmlist,bbox=detector.findposition(img)
    # print(lmlist)
    #2. get the tip of index and middle fingers
    if len(lmlist)!=0:
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        # print(x1,y1)
        # print(x2,y2)
    #3. check which fingers are up
    # fingers=detector.fingersUp()
    # print(fingers)
    fingers=detector.fingersUp()
    print(fingers)

    # print(fingers)
    cv2.rectangle(img, (300, 50), (600,300), (255, 0, 255), 2)
    #4. only index fingers: moving mode
    if fingers[1]==1 and fingers[2]==0:

    #5. convert coordinates
        x3=np.interp(x1,(300,600),(0,wscr))
        y3=np.interp(y1,(50,300),(0,hscr))
        # 6. smoothen values
        clocx=plocx+(x3-plocx)/smoothing
        clocy=plocy+(y3-plocy)/smoothing
        # 7. Move the mouse
        py.moveTo(x3,y3)
        cv2.circle(img,(x1,y1),15,(255,0,0),cv2.FILLED)
        plocx,plocx=clocx,clocy

    # 9. distance btw fingers
    length, img, info = detector.findDistance(8, 12, img)
    # print(length)

    # 8. both index and middle fingers are up : clicking mode
    # 10. click mouse if distance short
    if fingers[1] == 1 and fingers[2] == 1 and length<35:
       cv2.circle(img,(info[4],info[5]),15,(0,255,0),cv2.FILLED)
       py.click()
    # if fingers[0]==1 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0 and fingers[5]==0:
    #     py.scroll(-15)
    # if fingers[0] == 1 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0 and fingers[5]==0:
    #     py.scroll(15)

    #11. frame rate

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    #12. display




    cv2.imshow("Image",img)
    cv2.waitKey(1)
