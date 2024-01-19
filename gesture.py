from threading import Thread
import threading
import cv2
import time
import keyboard
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
import psutil
import numpy as np
import volume_control as vc
from collections import deque
from win32gui import GetWindowText, GetForegroundWindow
import brightness_control as bc
import presentation


thrd1 = None
 
    
class VideoGet:
    """
    Class that continuously gets imgs from a VideoCapture object
    with a dedicated thread.
    """
 
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        (self.grabbed, self.img) = self.cap.read()
        self.stopped = False

    def start(self):  
        print('in start')  
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while True:
            if not self.grabbed:
                print('continuing   not grabbed')
                continue
            else:
                if threading.main_thread().is_alive():
                    if thrd1 is None:
                        (self.grabbed, self.img) = self.cap.read()
                    elif thrd1.is_alive():
                        thrd1.join()
                    (self.grabbed, self.img) = self.cap.read()
                else:
                    print('stopped')
                    self.stop()
                    break

    def stop(self):
        print('ending grabbed')
        self.cap.release()
        self.stopped = True

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, img=None):
        self.img = img
        self.stopp = False

    def start(self):
        thrd2 = Thread(target=self.show, args=())
        thrd2.start()
        return self

    def show(self):
        while not self.stopp:
            if thrd1 is None:
                cv2.imshow("Video", self.img)
            elif thrd1.is_alive():
                thrd1.join()
            cv2.imshow("Video", self.img)

            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopp = True
  


def vol(img,detector,fingers,cap):
    volume_controller.set_volume(img, detector,fingers,cap) 

    print('thread ended')
    
def bright(img,detector,fingers,cap):
    brightness_control.set_brightness(img,detector,fingers,cap)
    print('brightness set')

def presentation_controlling(img,detector,fingers,cap):
    presentation_controller.control_presentation(img,detector,fingers,cap)
    

print("cahaali")
brightness_control = bc.brightness()
volume_controller = vc.volume()
presentation_controller = presentation.presentation_control()


def reset():
    # print('reset')
    lmlist = 0  
    pTime=0
    start_timer = None
    pressed = 0
    alt_pressed = 0
    screenshotted = 0
    yt_pressed = 0
    music_pressed = 0
    next_pressed = 0 
    pressed_prev = 0
    globals().update(locals()) 

wCam, hCam = 1280, 580
frameR = 100         #  frame Reduction
smoothness = 6
lmlist = 0

reset()

video_getter = VideoGet(0).start()
video_shower = VideoShow(video_getter.img).start()

detector = HandDetector(detectionCon=0.8,minTrackCon=0.6)

while True:
    
    # if thrd1.is_alive():
    #     thrd1.join
    current_window=GetWindowText(GetForegroundWindow()).lower()

    if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
        print('stopping')
        video_getter.stop() 
        # video_shower.stop()
        cv2.destroyAllWindows()
        # break
    cap = video_getter.cap
    img = video_getter.img
    # mediappe.start_detect(img)
    img = cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    # lmList, bbox = detector.findPosition(img)
    # print(psutil.cpu_times_percent())
    

    if hands == []:
        reset()

        if start_timer is None:
            start_timer=time.time()
        else:
            pass
        
        

    if hands:
        hand = hands[0]
        lmlist = hand["lmList"]
        hand_Type = hand["type"]
        if lmlist == 0:
            time.sleep(0.003)
            lmlist = 1
        if start_timer is not None:
            tm = (time.time())-start_timer
            
            start_timer = None
        
        fingers = detector.fingersUp(hand)
        cv2.rectangle(img, (frameR, 5),(wCam-frameR,hCam-frameR),(255,0,255),2)
        fings_up = [x for x in range(len(fingers)) if fingers[x]==1 and x != 0]

        length_pause, lineInfo_pause,img = detector.findDistance(lmlist[12][0:2],lmlist[16][0:2], img)
       
        length_thm_fing, lineInfo_thmfin,img = detector.findDistance(lmlist[4][0:2],lmlist[5][0:2], img)

        prev_length, lineInfo_next_trak,img = detector.findDistance(lmlist[4][0:2],lmlist[17][0:2],img)
        next_length, lineInfo_next_trak,img = detector.findDistance(lmlist[4][0:2],lmlist[5][0:2],img)
        
        
        

        if fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            pressed = 0
            print('in play-pause')
            if fingers[0] == 0 and fingers[1] == 1 and fingers[4] == 1 and fingers[2] == 0 and fingers[3] == 0 :
                # print('clicking play')
                if yt_pressed == 0 or music_pressed == 0:
                    keyboard.press_and_release('play/pause media')
                    print('pressed A    N   Y   music')
                    yt_pressed = 1
                    music_pressed = 1
            
            if ('youtube' in current_window or 'groove' in current_window or 'vlc' in current_window) and fingers[0] == 0 and fingers[1] == 1 and fingers[4] == 1 and fingers[2] == 0 and fingers[3] == 0:
                
                
                if 'youtube' in current_window and yt_pressed == 0:
                    print('pressed yt')
                    keyboard.press_and_release('k')
                    yt_pressed = 1
                if 'groove' in current_window and music_pressed == 0 or 'vlc' in current_window:
                    keyboard.press_and_release('space')
                    music_pressed = 1
                    print('pressed any music')
 
            ###############################################################
            ##          playback CONTROL
            ###############################################################

        
        if fingers[0]==1 and (fingers[1] and fingers[2] and fingers[3] and fingers[4]) == 1 and prev_length<=30: 
            pressed_prev = 0
            if next_pressed==0:
                keyboard.press_and_release('next_track')
                next_pressed=1


        if fingers[0] == 1 and len(fings_up)==0:
            next_pressed = 0 
            if pressed_prev==0:
                keyboard.press_and_release('previous_track')
                pressed_prev=1
        
        if len(fings_up) == 4 and length_thm_fing <=35 and length_pause>=50:
            if screenshotted == 0:
                keyboard.press_and_release('win+prtscn')
                screenshotted = 1

            
            ###############################################################
            ##          VOLUME CONTROL
            ###############################################################
 
        if fingers[0] == 0 and fingers[1]==1 and fingers[4] == 0 and fingers[2]==0 and fingers[3]==0:
            print("in volume")
            pressed = 0
            screenshotted = 0
            yt_pressed = 0
            music_pressed = 0
            next_pressed = 0 
            pressed_prev = 0
            # dqX.clear()
            # dqY.clear()
            clear=1
            thrd1 = threading.Thread(target=vol,args=(img, detector,fingers,cap))
            thrd1.start()
            thrd1.join()
            print('rejoin')

            ###############################################################
            ##          BRIGHTNESS CONTROL
            ###############################################################

        if fingers[0] == 0 and fingers[1]==1 and fingers[4] == 0 and fingers[2]==1 and fingers[3]==0 and fingers[0] != 1:
            pressed = 0
            yt_pressed = 0
            music_pressed = 0
            screenshotted = 0
            next_pressed = 0 
            pressed_prev = 0
            # dqX.clear()
            # dqY.clear()
            clear=1
            thrd1 = threading.Thread(target=bright,args=(img, detector,fingers,cap))
            thrd1.start()
            thrd1.join()
            print('rejoin')



            ###############################################################
            ##          PRESENTATION CONTROL
            ###############################################################


        if "slide show" in current_window:
            pressed = 0
            yt_pressed = 0
            music_pressed = 0
            screenshotted = 0
            next_pressed = 0 
            pressed_prev = 0
            thrd1 = threading.Thread(target=presentation_controlling,args=(img, detector,fingers,cap))
            thrd1.start()
            thrd1.join()
            print('rejoin')


        if len(fings_up)==4 and fingers[0] == 0 and next_length>=40:
            reset()


    video_shower.img = img
    