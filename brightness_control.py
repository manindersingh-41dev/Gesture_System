import screen_brightness_control as sbc
import cv2
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
# import pycaw
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from video_get import VideoGet


###################

class brightness():
    def __init__(self,mode=False, maxHands=1, detectionCon =0.75, minTrackCon = 0.5):
        self.mode= mode
        self.maxHands = maxHands
        self.detectionCon= detectionCon
        self.trackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20]


    def set_brightness(self,img, detector, fingers,cap):
        pTime = 0
        

        
        # volume.GetMute()
        # volume.GetMasterVolumeLevel()
        


        minbright = 0
        maxbright = 100
        area = 0

        # video_getter = VideoGet(1).start()
        hands,img = detector.findHands(img)
        if hands:
            fingers = detector.fingersUp(hands[0])
        
            while fingers[4]==0:
                success,img = cap.read()
                # img = cv2.flip(img,1)
                hands,img = detector.findHands(img,flipType=False)
                

                if hands:
                    hand = hands[0]
                    bbox = hand["bbox"]
                    area = (bbox[2]*bbox[3])//100
                    lmlist = hand["lmList"]
                    
                    
                    if 180<area<1200:
                        # print('yes')
                        length, img, lineInfo = detector.findDistance(lmlist[4][0:2],lmlist[8][0:2], img)
                        

                        
                        brightbar = np.interp(length,[20,210],[400,150])
                        brightperc = np.interp(length,[20,210],[0,100])
                        
                        
                        # volume.SetMasterVolumeLevel(vol, None)
                        #smoothness
                        smoothness = 2
                        brightperc = smoothness * round(brightperc/smoothness)

                        #check fingers up

                        fingers = detector.fingersUp(hand)
                        print('brightness',brightperc)
                        # print(fingers)
                        if fingers[0] == 0 and fingers[1]==1 and fingers[4] == 0 and fingers[2]==1 and fingers[3]==0:
                            try:
                                sbc.set_brightness(brightperc)
                            except Exception:
                                print('exception')
                                pass
                
                if hands == []:
                    break
