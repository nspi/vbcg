#!/usr/bin/env python
# camera.py - tool for reading video from a OpenCV-compatible camera

import cv2
import numpy as np
import logging

class camera():

    numberOfCameras = None

    def __init__(self):
        logging.info("Camera Object was initialized")

        # count the cameras available (idea from http://stackoverflow.com/a/30384945)
        # appearently there is still no OpenCV function (https://github.com/opencv/opencv/issues/4269)

        n = 0

        for i in range(5):
            try:
                cap = cv2.VideoCapture(i)
                ret, frame = cap.read()
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cap.release()
                cv2.destroyAllWindows()
                n += 1
            except:
                cap.release()
                cv2.destroyAllWindows()
                break

                tmp_str = "Found %d OpenCV-compatible cameras" % (n)
                logging.info(tmp_str)

        self.numberOfCameras = n

    def getNumberOfCameras(self):
        return self.numberOfCameras

    def set_camera(self,cameraIndex):

        # Initialize camera
        vs = cv2.VideoCapture(cameraIndex)

        # Get first frame
        ret, first_frame = vs.read()

        # Compute size
        sizeFrameX = np.size(first_frame, 0)
        sizeFrameY = np.size(first_frame, 1)

        # Return size
        return np.matrix([sizeFrameX, sizeFrameY])