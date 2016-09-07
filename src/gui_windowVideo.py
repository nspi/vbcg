#!/usr/bin/env python
# -*- coding: ascii -*-
"""gui_windowVideo.py - GUI element: frame that displays video"""

from defines import *
from PIL import Image
from PIL import ImageTk

import Tkinter as Tk
import threading
import numpy as np
import logging
import cv2
import settings
import os
import datetime

# Initialize global variables
root = None


class WindowVideo(Tk.Frame):
    """In this frame the video stream is shown"""

    def __init__(self, parent, tk_root, thread, cam, roi, statusbar):

        # Store variables
        global root
        self.root = tk_root
        self.parent = parent
        self.first_frame = True
        self.faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

        # Save camera object
        self.cameraInstance = cam

        # Save thread object
        self.threadInstance = thread

        # Save ROI toolbar object
        self.roiToolbarInstance = roi

        # Save statusbar instance
        self.statusbarInstance = statusbar

        # Initialize threading event for display of trigger symbol
        self.eventShowTrigger = threading.Event()

        # A counter that is used to determine how long the symbol is shown
        self.counterShownTriggerSymbol = 0

        # Initialize variable that contains HR
        self.HeartRateText = ' '

        # Create GUI
        self.__create_gui()

        # Get current settings
        self.curr_settings = settings.get_parameters()

        # Create variable to adjust thread sleeping time to desired FPS
        self.sleep_time = 1000 / self.curr_settings[IDX_FPS]

        # Start frame display as thread
        self.frameCounter = 0
        self.displayThread = threading.Thread(target=self.__show_image)
        self.displayThread.start()

        # Start FPS computation thread
        self.FPS = 0
        self.frameCounterLastValue = 0
        self.fpsCounterThread = threading.Thread(target=self.__compute_fps)
        self.fpsCounterThread.start()

    def __create_gui(self):
        """Create GUI elements and add them to root widget"""

        self.video_frame = Tk.Frame(root, width=500, height=400)
        self.video_frame.config(background="gray")
        self.video_frame.pack()
        self.lmain = Tk.Label(self.video_frame)
        self.lmain.pack()

    def __show_image(self):
        """Get frame from camera and display it"""

        # Get current settings
        self.curr_settings = settings.get_parameters()

        # Get current frame
        self.isTrueFrame, self.frame = self.cameraInstance.get_frame()

        # Check if first frame is received
        if self.isTrueFrame & self.first_frame:

            # Disable RGB selection button
            self.roiToolbarInstance.disable_color_channel_selection()

            # If first frame from camera is received store dimensions
            x_max = np.size(self.frame, 0)
            y_max = np.size(self.frame, 1)
            self.roiToolbarInstance.set_roi(0, x_max, 0, y_max)

            self.first_frame = False
            self.frameCounter += 1
            logging.info("First frame from webcam was received and ROI was adjusted")

            # If first frame from camera is received and the user wants to store frames, create folder
            if self.curr_settings[IDX_FRAMES]:
                self.directory = os.path.join(os.getcwd(), 'data',
                                              datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S'))
                # for window compatibility, colon has been replaced by dot
                os.makedirs(self.directory)
                logging.info('Folder was created for storing frames')

        # Process all following frames
        elif self.isTrueFrame:

            # Increase frame counter
            self.frameCounter += 1

            # Use Viola Jones Algorithm for Face Detection
            if self.curr_settings[IDX_FACE]:
                frame_bw = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceCascade.detectMultiScale(frame_bw, scaleFactor=1.1, minNeighbors=5,
                                                          minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
                for (x, y, w, h) in faces:
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    self.roiToolbarInstance.set_roi(y, y + h, x, x + w)

            # Otherwise: Use manual ROI input
            else:
                x_min, x_max, y_min, y_max = self.roiToolbarInstance.get_roi()
                cv2.rectangle(self.frame, (y_min, x_min), (y_max, x_max), (0, 255, 0), 2)

            # Store frame on hard disk
            if self.curr_settings[IDX_FRAMES]:
                file_name = "frame%d.jpg" % self.frameCounter
                cv2.imwrite(os.path.join(self.directory, file_name), cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))

        # Display icon
        current_location = os.path.dirname(os.path.realpath(__file__)) + os.sep

        # Heart icon
        if self.curr_settings[IDX_ALGORITHM] == 0:
            # Add heart icon
            heart_location = current_location + 'data/heart.png'
            self.frame = self.__add_figure_to_frame(self.frame, heart_location)
            # Add text that displays Heart Rate
            cv2.putText(self.frame, self.HeartRateText, (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Heartbeat icon
        elif self.curr_settings[IDX_ALGORITHM] == 1:

            # If signal processing algorithm set trigger event
            if self.eventShowTrigger.is_set():
                # Counter used to decide how long icon is shown
                self.counterShownTriggerSymbol += 1
                # Add heart icon
                heart_location = current_location + 'data/heartbeat.png'
                self.frame = self.__add_figure_to_frame(self.frame, heart_location)
                # Clear event if symbol has been shown for approx 1/3 sec
                if self.counterShownTriggerSymbol >= self.FPS / 3:
                    self.counterShownTriggerSymbol = 0
                    self.eventShowTrigger.clear()

        # Display frame
        self.frameConverted = Image.fromarray(self.frame)
        self.imgTK = ImageTk.PhotoImage(image=self.frameConverted)
        self.lmain.imgtk = self.imgTK
        self.lmain.configure(image=self.imgTK)

        # Update values in statusbar
        self.statusbarInstance.set_frame_counter(self.get_frame_counter())
        self.statusbarInstance.set_fps_counter(self.FPS)

        # Repeat thread immediately
        self.video_frame.after(1, lambda: self.__show_image())

    def __compute_fps(self):
        """Compute FPS"""
        self.FPS = self.get_frame_counter() - self.frameCounterLastValue

        # Update value
        self.frameCounterLastValue = self.get_frame_counter()

        # Repeat thread
        self.video_frame.after(1000, lambda: self.__compute_fps())

    def __add_figure_to_frame(self, frame, figure_location):
        """This function is used to add a file from hard disk to the figure
        Algorithm source: http://docs.opencv.org/trunk/d0/d86/tutorial_py_image_arithmetics.html
        """
        # Get size of frame
        height, width, channels = frame.shape

        # Only add icon when the frame is big enough
        if height >= 100 and width >= 100:

            # Load heart icon
            icon_heart = cv2.imread(figure_location)
            # Convert to RGB
            icon_heart = cv2.cvtColor(icon_heart, cv2.COLOR_BGR2RGB)
            # Create ROI
            rows, cols, channels = icon_heart.shape
            roi = frame[:rows, :cols, :]
            # Convert heart to greyscale
            icon_heart_gray = cv2.cvtColor(icon_heart, cv2.COLOR_RGB2GRAY)
            # Create mask and inverse mask with binary threshold
            ret, mask = cv2.threshold(icon_heart_gray, 10, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            # Background: Original frame with inverse mask
            frame_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
            # Foreground: Heart with normal mask
            icon_heart_fg = cv2.bitwise_and(icon_heart, icon_heart, mask=mask)
            # Add heart icon to frame
            icon_heart_final = cv2.add(frame_bg, icon_heart_fg)
            frame[:rows, :cols, :] = icon_heart_final

        return frame

    # Setter and getter following

    def get_frame_counter(self):
        """Returns number of frames shown so far"""
        return self.frameCounter

    def set_heart_rate_text(self, newHR):
        """Set Heart Rate Text"""
        self.HeartRateText = newHR

    def display_heart_trigger(self):
        """Activate event so that the heart as a symbol for a trigger is shown"""
        self.eventShowTrigger.set()
