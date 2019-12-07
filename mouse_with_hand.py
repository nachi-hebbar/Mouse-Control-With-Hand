import cv2
import numpy as np
from pynput.mouse import Button, Controller
import tkinter as tk
mouse=Controller()
root = tk.Tk()
screenx = root.winfo_screenwidth()
screeny = root.winfo_screenheight()
(camx,camy)=(320,240)
lowerBound=np.array([110,150,100])#blue contour
upperBound=np.array([120,200,200])
cam= cv2.VideoCapture(0)
#ret, img = cam.read() 


kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
pinchFlag=0
while True:

    ret, img=cam.read()
    img=cv2.resize(img,(340,220))
    hand_cascade=cv2.CascadeClassifier("hand1.xml")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #hands = hand_cascade.detectMultiScale(gray, 1.5, 5)
    hands = hand_cascade.detectMultiScale(gray, 1.2, 5)
    #print("No of faces found:",#len(faces))
    a=len(hands)
  
    #for (x,y,w,h) in hands:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology operation
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)#to remove background white noises in the camera
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    maskFinal=maskClose
    contours,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    print(len(hands))
    if(len(hands)==1):#if only one contour is present
        #print("hello")
        #x,y,w,h=cv2.boundingRect(hands)
        if(pinchFlag==0):
            pinchFlag=1
            mouse.press(Button.left)
        for (x,y,w,h) in hands:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
            cx=x+w//2
            cy=y+h//2
            cv2.circle(img,(cx,cy),(w+h)//4,(0,0,255),2)
            mouseLocation=(screenx-(cx*screenx/camx), cy*screeny/camy)
            mouse.position=mouseLocation
       # while mouse.position!=mouseLocation:
            #pass
            if(len(hands==2)):
                if(pinchFlag==1):
                    pinchFlag=0
                    mouse.release(Button.left)
                mouse.position=mouselocation
    cv2.imshow("cam",img)

    #cv2.imshow("mask",mask)
    cv2.waitKey(5)
