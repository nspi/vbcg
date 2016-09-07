#!/usr/bin/env python
# -*- coding: ascii -*-
"""video.py - tool for reading video from a OpenCV-compatible camera"""

import cv2
import numpy as np
import logging
import threading
import settings
import time
import datetime
import os

from defines import *


class VideoThread(threading.Thread):
    """ This thread acquires frames from a camera or from hard disk and provides them to others.
        When the user presses the ''x'' button, the connection to the camera is closed.
    """

    def run(self):
        """ This block is performed until the user ends the program"""

        # Has a connection been established to the camera or the hard disk?
        connection_established = False

        # run() method of cameraThread waits for shutdown event
        while self.eventProgramEnd.is_set() is False:

            # Timer for dynamic FPS adjustment
            self.startTime = datetime.datetime.now()

            # Check if the user wants to read frames from hard disk or from camera
            if self.files is not None:

                # Check if connection has been established
                if connection_established is False:

                    # Check if the user has pressed the start button
                    user_pressed_start = self.eventUserPressedStart.wait(1)

                    if user_pressed_start:

                        logging.info("User pressed start and wants to use frames from hard disk")

                        # Create variable to adjust thread sleeping time to desired FPS
                        self.currSettings = settings.get_parameters()
                        self.FPS = self.currSettings[IDX_FPS]

                        # Set event for other threads
                        self.eventVideoReady.set()

                        # Set bool variable, so that the thread can start to capture frames
                        connection_established = True

                # Continuously capture frames until user ends program
                if self.eventVideoReady.is_set():

                    try:
                        # Construct file directory and name
                        curr_file = self.filesDir + os.sep + self.files[self.frameCounter]

                        # Read frame
                        self.currentFrame = cv2.imread(curr_file)

                        # Increase counter
                        self.frameCounter += 1

                    except IndexError:
                        logging.info("Reached last file.")

                    # Wait and start from beginning of thread
                    self.__wait_to_adjust_fps(self.startTime, datetime.datetime.now())

            # If the user did not choose frames from hard disk, use camera instead
            else:

                # Check if connection has been established
                if connection_established is False:

                    # Check if the user has pressed the start button
                    user_pressed_start = self.eventUserPressedStart.wait(1)

                    if user_pressed_start:

                        logging.info("User pressed start and wants to use the camera")

                        # Create variable to adjust thread sleeping time to desired FPS
                        self.currSettings = settings.get_parameters()
                        self.FPS = self.currSettings[IDX_FPS]

                        # Open connection to camera
                        self.__open_camera()

                        # Set event for other threads
                        self.eventVideoReady.set()

                        # Set bool variable, so that the thread can start to capture frames
                        connection_established = True

                        # Timer for dynamic FPS adjustment
                        self.startTime = datetime.datetime.now()

                # Continuously capture frames until user ends program
                if self.eventVideoReady.is_set():

                    # Read frame
                    ret, self.currentFrame = self.videoStream.read()

                # Wait and start from beginning of thread
                self.__wait_to_adjust_fps(self.startTime, datetime.datetime.now())

        # Shutdown reached: Close connection to camera if it was used
        if self.files is None:
            self.__close_camera()

    def __init__(self):
        """ Initialization of class. The system is scanned for OpenCV compatible cameras and variables are set """

        # Thread initialization
        threading.Thread.__init__(self)

        # Set camera to default value
        self.cameraIdx = 0

        # Event is activated when user presses ''start'' button
        self.eventUserPressedStart = threading.Event()

        # Event is activated when frames are received from camera or hard disk
        self.eventVideoReady = threading.Event()

        # Event is activated when user closed the application.
        self.eventProgramEnd = threading.Event()

        # Create variable to adjust thread sleeping time to desired FPS
        self.currSettings = settings.get_parameters()
        self.FPS = self.currSettings[IDX_FPS]

        # Initialize variables
        self.videoStream = self.startTime = None

        # A black frame that is displayed until the user has started the program
        self.currentFrame = np.zeros((480, 640, 3), np.uint8)

        # If the user wants to read frames from the hard disk, the directory and file names are stored here
        self.filesDir = None
        self.files = None

        # A counter of loaded frames, used for loading frames from hard disk
        self.frameCounter = 0

        # During init, the cameras available are counted (idea from http://stackoverflow.com/a/30384945)
        # apparently there is still no clean OpenCV-based solution (https://github.com/opencv/opencv/issues/4269)
        self.numberOfCameras = 0

        for i in range(2):
            cap = None
            try:
                cap = cv2.VideoCapture(i)
                ret, frame = cap.read()
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cap.release()
                cv2.destroyAllWindows()
                self.numberOfCameras += 1
            except:
                if cap is not None:
                    cap.release()
                    cv2.destroyAllWindows()
                break

            tmp_str = "Found " + str(self.numberOfCameras) + " OpenCV-compatible cameras"
            logging.info(tmp_str)

    def get_frame(self):
        """This function delivers frames from the camera or the hard disk for the GUI

            Returns:
            status -- False if user has not pressed ''start'' button. If pressed, returns True
            frame -- A black frame is the user has not pressed ''start'' button. Otherwise frame from camera or disk
        """

        # Waiting for the user to press the ''start'' button
        if self.eventVideoReady.is_set():

                # Read current frame from thread
                frame = self.currentFrame

                # Convert color to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Return status and frame
                return True, frame

        else:
            # Return false as status and black frame
            return False, np.zeros((480, 640, 3), np.uint8)

    def __wait_to_adjust_fps(self, start_time, end_time):
        # Compute difference to desired FPS
        self.diffTime = (end_time - start_time).total_seconds()
        self.waitTime = 1.0 / self.FPS - self.diffTime
        # If thread was too fast, wait
        if self.waitTime > 0:
            time.sleep(self.waitTime)

    def __open_camera(self):
        """This function initializes the desired camera"""
        self.videoStream = cv2.VideoCapture(int(self.cameraIdx))
        logging.info("The camera was initialized")

    def __close_camera(self):
        """This function releases the current camera"""
        if self.videoStream is not None:
            self.videoStream.release()
            logging.info("The camera was released")

    def close_camera_thread(self):
        """User pressed ''quit'' button, set events to that thread can end"""
        self.eventVideoReady.clear()
        self.eventProgramEnd.set()

    def store_frames_from_disk(self, directory, files):
        """This function stores the directory and files if the user wants to use frames from the hard disk"""
        self.filesDir = directory
        self.files = files

    def set_camera_idx(self, camera_index):
        """ Store index of camera that user has chosen using the GUI"""
        self.cameraIdx = camera_index
        logging.info("Camera index was set because user pressed start button")

    def get_number_of_cameras(self):
        """This function returns the number of available OpenCV cameras for the GUI"""
        return self.numberOfCameras

    def get_event_camera_ready(self):
        """ Getter for eventUserPressedStart"""
        return self.eventVideoReady

    def get_event_camera_chosen(self):
        """ Getter for eventUserPressedStart"""
        return self.eventUserPressedStart
