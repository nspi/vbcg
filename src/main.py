#!/usr/bin/env python
# main.py - the main program

import settings
import logger
import gui

from camera import camera


# Initialize logging
logger.init()

# Initialize camera
cameraInstance = camera()

# Initialize GUI
gui.init(cameraInstance)