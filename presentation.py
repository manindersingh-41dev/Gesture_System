from threading import Thread
import threading
import cv2
import time
import keyboard
import mediapipe as mp
# import hand_Detection_module as htm
import psutil
import numpy as np
from collections import deque
from win32gui import GetWindowText, GetForegroundWindow
thrd1 = None
import pyautogui
from cvzone.HandTrackingModule import HandDetector

class presentation_control():
    def __init__(self,mode=False, maxHands=1, detectionCon =0.75, minTrackCon = 0.6):
        self.mode= mode
        self.maxHands = maxHands
        self.detectionCon= detectionCon
        self.trackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20]
    
    def control_presentation(self,img,detector,fingers,cap):
        next_pressed = 0
        pressed_prev =0
        
        hands,img = detector.findHands(img,flipType=False)
        current_window=GetWindowText(GetForegroundWindow()).lower()
        # print(hands)
        while "slide show" in current_window:
            current_window=GetWindowText(GetForegroundWindow()).lower()
            success,img = cap.read()
            img = cv2.flip(img,1)
            hands,img = detector.findHands(img,flipType=False)

            if hands == []:
                # print("here")
                next_pressed = 0
                pressed_prev = 0

            if hands:
                hand = hands[0]
                handType = hand["type"]
                # print(handType)
                fingers = detector.fingersUp(hand)
                fings_up = [x for x in range(len(fingers)) if fingers[x]==1 and x != 0]
                # print(fingers[1]," ",fingers[0])
                
                
                if fings_up == [1,2,3,4] and fingers[0] == 0 and (next_pressed !=0 or pressed_prev!=0):
                    print("reset")
                    next_pressed = 0 
                    pressed_prev = 0

                if handType=="Right":
                    if fingers[0]==0 and fingers[1]==1 and fingers[4]==0 and fingers[2]==0 and fingers[3]==0:
                        if next_pressed==0:
                            keyboard.press_and_release("right")
                            print("next")
                            next_pressed=1
                            pressed_prev=0
                        else:
                            pass
                

                if handType=="Left":
                    if fingers[0]==0 and fingers[1]==1 and fingers[4]==0 and fingers[2]==0 and fingers[3]==0:
                        if pressed_prev==0:
                            keyboard.press_and_release("left")
                            pressed_prev = 1
                            next_pressed=0
                            print("prev")

            # video_shower.img = img

            
