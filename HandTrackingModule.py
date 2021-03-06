import cv2
import mediapipe as mp
import time
import math
import numpy as np


class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxhands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxhands,self.detectionCon,self.trackCon)

        self.mpDraw=mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]

    def findhands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        # print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handlms,self.mpHands.HAND_CONNECTIONS)

        return img

    def findposition(self,img,handNo=0,draw=True):
        xlist=[]
        ylist=[]
        bbox=[]
        self.lmlist=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                # print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                xlist.append(cx)
                ylist.append(cy)
                # print(id,cx,cy)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
            xmin,xmax=min(xlist),max(xlist)
            ymin,ymax=min(ylist),max(ylist)
            bbox=xmin,ymin,xmax,ymax

            if draw:
                cv2.rectangle(img,(xmin-20,ymin-20),(xmax+20,ymax+20),(0,255,0),2)
        # print(self.lmlist)
        return self.lmlist,bbox

    def findDistance(self,p1,p2,img,draw=True,radius=15,thikness=3):
        x1,y1=self.lmlist[p1][1:]
        x2,y2=self.lmlist[p2][1:]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),thickness)
            cv2.circle(img, (x1,y1), radius, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2,y2), radius, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx,cy), radius, (0, 0, 255), cv2.FILLED)
        length=math.hypot(x2-x1,y2-y1)

        return length,img,[x1,y1,x2,y2,cx,cy]



    def fingersUp(self):
        fingers=[]
        #thumb
        if self.lmlist[self.tipIds[0]][2] < self.lmlist[self.tipIds[0]+1][2] or self.lmlist[self.tipIds[0]][2] < self.lmlist[self.tipIds[0]+5][2]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        totalfingers=fingers.count(1)
        # print(totalfingers)
        # print(fingers)
        return fingers



    

if __name__=="__main__":
    ptime=0
    ctime=0
    cap=cv2.VideoCapture(0)
    detector=handDetector()
    while True:
        success,img=cap.read()
        img=detector.findhands(img)
        lmlist,bbox=detector.findposition(img)
        if len(lmlist)!=0:
            print(lmlist[4])


        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow("Image",img)
        cv2.waitKey(1)
