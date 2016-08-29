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

# Configure logging
logger.init()

# Initialize camera thread
videoThread = video.VideoThread()
# Start camera thread
videoThread.start()

# Initialize gui
guiThread = gui.GUI()
# Add camera thread to gui
guiThread.setVideoThread(videoThread)
# Start gui
guiThread.start()
