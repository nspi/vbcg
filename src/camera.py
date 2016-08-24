#!/usr/bin/env python
# camera.py - tool for reading video from a OpenCV-compatible camera

import cv2
import numpy as np
import logging
import threading

# Initialize variables
eventCameraChosen = eventCameraReady = eventProgramEnd = None
videoStream = numberOfCameras = cameraIdx = None


class CameraThread(threading.Thread):

    def run(self):
        # This threads provides frames from a camera or from hard disk
        # When using frames from disk, it ends after initialization. When using a camera, it runs continuously.
        # When the user presses the ''quit'' button, the connection to the camera is closed.

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
                        # Set event so that this thread exits because it slows down the application
                        self.eventProgramEnd.set()

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
                        logging.info("Camera is ready. Other processes can acquire frames.")
                        # Set bool variable, so that the thread can start to capture frames
                        connectionEstablished = True

                # Continuosly capture frames until user ends program
                if self.eventVideoReady.is_set():
                    ret, self.currentFrame = self.videoStream.read()


        # Close connection to camera if it was used
        if self.files is None:
            self.__closeCamera()

    def __init__(self):
        # Thread initialization
        threading.Thread.__init__(self)

        # During init, the cameras available are counted (idea from http://stackoverflow.com/a/30384945)
        # appearently there is still no clean OpenCV-based solution (https://github.com/opencv/opencv/issues/4269)
        # n = 0
        #
        # for i in range(5):
        #     try:
        #         cap = cv2.VideoCapture(i)
        #         ret, frame = cap.read()
        #         cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #         cap.release()
        #         cv2.destroyAllWindows()
        #         n += 1
        #     except:
        #         cap.release()
        #         cv2.destroyAllWindows()
        #         break
        #
        #         tmp_str = "Found %d OpenCV-compatible cameras" % (n)
        #         logging.info(tmp_str)

        global videoStream
        self.videoStream = None
        self.numberOfCameras = 2
        self.currentFrame = np.zeros((480, 640, 3), np.uint8)
        self.eventProgramEnd = threading.Event()
        self.filesDir = None
        self.files = None
        self.frameCounter = 0

    def __openCamera(self):
        # This function initializes the desired camera
        global videoStream
        self.videoStream = cv2.VideoCapture(int(self.cameraIdx))
        logging.info("The camera was initialized")

    def __closeCamera(self):
        # This function releases the current camera
        global videoStream
        if self.videoStream is not None:
            self.videoStream.release()
            logging.info("The camera was released")

    def closeCameraThread(self):
        # User pressed ''quit'' button, set events to that thread can end
        self.eventVideoReady.clear()
        self.eventProgramEnd.set()

    def setCameraIdx(self, cameraIndex):
        global cameraIdx
        self.cameraIdx = cameraIndex
        logging.info("Camera index was set because user pressed start button")

    def getNumberOfCameras(self):
        # This function returns the number of available OpenCV cameras
        return self.numberOfCameras

    def getFrame(self):
        # This function delivers black frames until the user pressed ''start''
        global videoStream

        if self.eventVideoReady.is_set():

            # Get frames from live webcam
            if self.files is None:
                frame = self.currentFrame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return True, frame

            # Get frames from hard disk
            else:
                try:
                    currFile = self.filesDir + '/' + self.files[self.frameCounter]
                    frame = cv2.imread(currFile)
                    self.frameCounter += 1
                    return True, frame
                except IndexError:
                    logging.info("Reached last file.")
                    return False, np.zeros((480, 640, 3), np.uint8)

        else:

            return False, np.zeros((480, 640, 3), np.uint8)

    def getResolution(self):
        # This function returns the resolution the camera frames
        global videoStream
        ret, frame = self.videoStream.read()
        return np.size(frame)

    def storeFramesFromDisk(self, directory, files):
        # This function stores the directory and files if the user wants to use frames from the hard disk
        self.filesDir = directory
        self.files = files

    # Setter and getter for the threading events
    def setEventCameraChosen(self, event):
        global eventCameraChosen
        self.eventUserPressedStart = event

    def setEventCameraReady(self, event):
        self.eventVideoReady = event

    def getEventCameraReady(self):
        global eventCameraReady
        return self.eventVideoReady

    def getEventCameraChosen(self):
        global eventCameraChosen
        return self.eventUserPressedStart
