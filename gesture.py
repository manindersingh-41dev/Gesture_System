from threading import Thread
import threading
import cv2
import time
import keyboard
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
import psutil
import numpy as np
from collections import deque


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
  
wCam, hCam = 1280, 580
frameR = 100         #  frame Reduction
smoothness = 6
lmlist = 0


video_getter = VideoGet(0).start()
video_shower = VideoShow(video_getter.img).start()

while True:
    if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
        print('stopping')
        video_getter.stop() 
        cv2.destroyAllWindows()

    cap = video_getter.cap
    img = video_getter.img
    # mediappe.start_detect(img)
    img = cv2.flip(img,1)



    video_shower.img = img