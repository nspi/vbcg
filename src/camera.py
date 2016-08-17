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
        # The thread waits until a camera is ready and then provides frames.
        # When the user presses the ''quit'' button, the connection to the camera is closed
        cameraConnectionEstablished = False

        # run() method of cameraThread waits for shutdown event
        while self.eventProgramEnd.is_set() is False:

            # Check if connection to camera has been established
            if cameraConnectionEstablished is False:

                logging.info("Camera thread was started. Waiting for EventCameraChosen.")
                UserChoseCamera = self.eventCameraChosen.wait(1)

                if UserChoseCamera:

                    # Open connection to camera
                    self.__openCamera()
                    # Set event for other threads
                    self.eventCameraReady.set()
                    logging.info("Camera is ready. Other processes can acquire frames.")
                    # Set bool variable, so that the thread can start to capture frames
                    cameraConnectionEstablished = True

            # Continuosly capture frames until user ends program
            if self.eventCameraReady.is_set():
                ret, self.currentFrame = self.videoStream.read()

        # Close connection to camera
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
        self.eventCameraReady.clear()
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

        if self.eventCameraReady.is_set():
            frame = self.currentFrame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return True, frame
        else:
            return False, np.zeros((480, 640, 3), np.uint8)

    def getResolution(self):
        # This function returns the resolution the camera frames
        global videoStream
        ret, frame = self.videoStream.read()
        return np.size(frame)

    def __getStatus(self):
        # This function returns true when the user has chosen a camera by clicking ''start''
        if self.eventCameraChosen is not None:
            return True
        else:
            return False

    # Setter and getter for the threading events
    def setEventCameraChosen(self, event):
        global eventCameraChosen
        self.eventCameraChosen = event

    def setEventCameraReady(self, event):
        self.eventCameraReady = event

    def getEventCameraReady(self):
        global eventCameraReady
        return self.eventCameraReady

    def getEventCameraChosen(self):
        global eventCameraChosen
        return self.eventCameraChosen
