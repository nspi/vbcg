#!/usr/bin/env python
# gui.py - GUI element: frame that displays video

import Tkinter as Tk
import threading
import Image
import ImageTk
import numpy as np
import logging
import cv2
import settings

from defines import *

# Initialize global variables
root =  None

class WindowVideo(Tk.Frame):
    # In this frame the video stream is shown

    def __init__(self, parent, tk_root, thread, cam, roi):

        # Store variables
        global root
        self.root = tk_root
        self.first_frame = True
        self.faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

        # Save camera object
        self.cameraInstance = cam

        # Save thread object
        self.threadInstance = thread

        # Save ROI toolbar object
        self.roiToolbarInstance = roi

        # Create GUI
        self.__create_gui()

        # Create variable to adjust thread sleeping time to desired FPS
        self.sleep_time = 1000/VAL_FPS

        # Start frame display as thread
        self.frameCounter = 0
        self.displayThread = threading.Thread(target=self.__showImage)
        self.displayThread.start()

        # Start FPS computation thread
        self.FPS = 0
        self.frameCounterLastValue = 0
        self.fpsCounterThread = threading.Thread(target=self.__computeFPS)
        self.fpsCounterThread.start()

    def __create_gui(self):
        # Create GUI elements and add them to root widget

        self.video_frame = Tk.Frame(root, width=500, height=400)
        self.video_frame.config(background="gray")
        self.video_frame.pack()
        self.lmain = Tk.Label(self.video_frame)
        self.lmain.pack()

    def __showImage(self):
        # Get frame from camera and display it

        # Get current settings
        self.curr_settings = settings.get_parameters()

        # Get current frame
        self.isTrueFrame, self.frame = self.cameraInstance.getFrame()

        if self.isTrueFrame & self.first_frame:
            # If first frame from camera is received store dimensions

            x_max = np.size(self.frame, 0)
            y_max = np.size(self.frame, 1)
            self.roiToolbarInstance.setROI(0, x_max, 0, y_max)
            self.first_frame = False
            self.frameCounter += 1
            logging.info("First frame from webcam was received and ROI was adjusted")

        elif self.isTrueFrame:
            # If frame is received, use Viola-Jones algorithm or manual ROI definition to crop frame

            if self.curr_settings[IDX_FACE]:
                #Use Viola-Jones
                frameBW = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceCascade.detectMultiScale(frameBW,scaleFactor=1.1,minNeighbors=5,
                                                     minSize=(30, 30),flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
                for (x, y, w, h) in faces:
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    self.roiToolbarInstance.setROI(y, y + h, x, x + w)
            else:
                # Otherwise: Use manual ROI input
                x_min,x_max,y_min,y_max = self.roiToolbarInstance.getROI()
                cv2.rectangle(self.frame,(y_min,x_min),(y_max,x_max),(0, 255, 0), 2)

            self.frameCounter += 1

        self.frameConverted = Image.fromarray(self.frame)
        self.imgTK = ImageTk.PhotoImage(image=self.frameConverted)
        self.lmain.imgtk = self.imgTK
        self.lmain.configure(image=self.imgTK)

        # This block dynamically adjusts the sleep time of this thread. The aim is to converge to the desired FPS of
        # the used camera which can not be fixed due to the workload of the other threads
        if (self.isTrueFrame) and ((self.get_frameCounter() % 25) == 0):
            currentFPS = self.FPS

            if currentFPS < VAL_FPS:
                self.sleep_time -= 1
            elif currentFPS > VAL_FPS:
                self.sleep_time += 1


        # Repeat thread
        self.video_frame.after(self.sleep_time, lambda: self.__showImage())

    def __computeFPS(self):
        # Compute FPS
        self.FPS = self.get_frameCounter()-self.frameCounterLastValue

        # Update value
        self.frameCounterLastValue = self.get_frameCounter()

        # Repeat thread
        self.video_frame.after(1000, lambda: self.__computeFPS())

    def get_frameCounter(self):
        return self.frameCounter

    def get_FPS(self):
        return str(self.FPS)
