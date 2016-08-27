#!/usr/bin/env python
# -*- coding: ascii -*-
""" main.py - here starts everything

    The program logic is divided in two threads:
        (1) a video thread that acquires frames from the camera or hard disk
        (2) a thread that manages the graphical user interaface and signal processing

    Please note that both threads have different processing speeds, denoted in the statusbar.
"""

import logger
import gui
import video
import threading

# Configure logging
logger.init()

# Create events for thread communication
eventUserPressedStart = threading.Event()           # is activated when user presses ''start'' button
eventVideoIsReady = threading.Event()               # is activated when frames are received from camera or hard disk

# Initialize camera thread
videoThread = video.VideoThread()
# Add events to camera thread
videoThread.setEventUserPressedStart(eventUserPressedStart)
videoThread.setEventVideoReady(eventVideoIsReady)
# Start camera thread
videoThread.start()

# Initialize gui
guiThread = gui.GUI()
# Add camera thread to gui
guiThread.setVideoThread(videoThread)
# Start gui
guiThread.start()
