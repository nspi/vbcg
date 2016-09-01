#!/usr/bin/env python
# -*- coding: ascii -*-
""" main.py - here starts everything

    The program logic is divided in four threads:

        VideoThread:
            (1) a thread that acquires frames from the camera / hard disk

        guiThread:
            (2) a thread that shows the current frame in the GUI
            (3) a thread that processes the current frame
            (4) a thread that shows the obtained signal in the GUI

        The GUI class contains all GUI elements which are defined in gui_*.py using Tkinter
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

# Add camera thread and start gui
guiThread.start(videoThread)
