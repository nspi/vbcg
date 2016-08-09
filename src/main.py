#!/usr/bin/env python
# main.py - the main program

import logger
import gui
import camera
import threading

# Configure logging
logger.init()

# Create events for thread communication
eventCameraChosen = threading.Event()           # is activated when user presses ''start'' button
eventCameraIsReady = threading.Event()          # is activated when camera receives frames

# Initialize camera thread
camThread = camera.cameraThread()
# Add events to camera thread
camThread.setEventCameraChosen(eventCameraChosen)
camThread.setEventCameraReady(eventCameraIsReady)
# Start camera thread
camThread.start()

# Initialize gui
gui = gui.GUI()
# Add camera thread to gui
gui.setCamera(camThread)
# Start gui
gui.start()
