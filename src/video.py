#!/usr/bin/env python
# -*- coding: ascii -*-
"""video.py - tool for reading video from a OpenCV-compatible camera"""

import cv2
import numpy as np
import logging
import threading
import sys
import os
import settings

from defines import *


class VideoThread(threading.Thread):
    """ This class acquires frames from a camera or from hard disk as a thread and provides them to others
        When the user presses the ''x'' button, the connection to the camera is closed.
    """

    def run(self):
        """ This block is performed until the user ends the program"""

        # Has a connection been established to the camera or the hard disk?
        connectionEstablished = False

        # run() method of cameraThread waits for shutdown event
        while self.eventProgramEnd.is_set() is False:

            # Check if the user wants to read frames from hard disk or from camera
            if self.files is not None:

                # Check if connection has been established
                if connectionEstablished is False:

                    # Check if the user has pressed the start button
                    userPressedStart = self.eventUserPressedStart.wait(1)

                    if userPressedStart:

                        logging.info("User pressed start and wants to use frames from hard disk")

                        # Set event for other threads
                        self.eventVideoReady.set()

                        # Set bool variable, so that the thread can start to capture frames
                        connectionEstablished = True

                # Continuosly capture frames until user ends program
                if self.eventVideoReady.is_set():

                    try:
                        # Construct file directory and name
                        currFile = self.filesDir + '/' + self.files[self.frameCounter]

                        # Read frame
                        self.currentFrame = cv2.imread(currFile)

                        # Increase counter
                        self.frameCounter += 1

                        # Wait
                        cv2.waitKey(int(self.sleep_time))

                    except IndexError:
                        logging.info("Reached last file. Restarting program.")
                        os.execl(sys.executable, sys.executable, *sys.argv)

            # If the user did not choose frames from hard disk, use camera instead
            else:

                # Check if connection has been established
                if connectionEstablished is False:

                    # Check if the user has pressed the start button
                    userPressedStart = self.eventUserPressedStart.wait(1)

                    if userPressedStart:

                        logging.info("User pressed start and wants to use the camera")

                        # Open connection to camera
                        self.__openCamera()

                        # Set event for other threads
                        self.eventVideoReady.set()

                        # Set bool variable, so that the thread can start to capture frames
                        connectionEstablished = True

                # Continuosly capture frames until user ends program
                if self.eventVideoReady.is_set():

                    # Read frame
                    ret, self.currentFrame = self.videoStream.read()

                    # Wait
                    cv2.waitKey(int(self.sleep_time))

        # Shutdown reached: Close connection to camera if it was used
        if self.files is None:
            self.__closeCamera()

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

        # Video stream object, is filled later
        self.videoStream = None

        # A black frame that is displayed until the user has started the program
        self.currentFrame = np.zeros((480, 640, 3), np.uint8)

        # If the user wants to read frames from the hard disk, the directory and file names are stored here
        self.filesDir = None
        self.files = None

        # Create variable to adjust thread sleeping time to desired FPS
        self.curr_settings = settings.get_parameters()
        self.sleep_time = 1000 / self.curr_settings[IDX_FPS]

        # A counter of loaded frames, used for loading frames from hard disk
        self.frameCounter = 0

        # During init, the cameras available are counted (idea from http://stackoverflow.com/a/30384945)
        # appearently there is still no clean OpenCV-based solution (https://github.com/opencv/opencv/issues/4269)
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


    def getFrame(self):
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

    def __openCamera(self):
        """This function initializes the desired camera"""
        global videoStream
        self.videoStream = cv2.VideoCapture(int(self.cameraIdx))
        logging.info("The camera was initialized")

    def __closeCamera(self):
        """This function releases the current camera"""
        global videoStream
        if self.videoStream is not None:
            self.videoStream.release()
            logging.info("The camera was released")

    def closeCameraThread(self):
        """User pressed ''quit'' button, set events to that thread can end"""
        self.eventVideoReady.clear()
        self.eventProgramEnd.set()

    # Setter and Getter following:

    def storeFramesFromDisk(self, directory, files):
        """This function stores the directory and files if the user wants to use frames from the hard disk"""
        self.filesDir = directory
        self.files = files

    def setCameraIdx(self, cameraIndex):
        """ Store index of camera that user has chosen using the GUI"""
        global cameraIdx
        self.cameraIdx = cameraIndex
        logging.info("Camera index was set because user pressed start button")

    def getNumberOfCameras(self):
        """This function returns the number of available OpenCV cameras for the GUI"""
        return self.numberOfCameras

    def getEventCameraReady(self):
        """ Getter for eventUserPressedStart"""
        global eventCameraReady
        return self.eventVideoReady

    def getEventCameraChosen(self):
        """ Getter for eventUserPressedStart"""
        global eventUserPressedStart
        return self.eventUserPressedStart
