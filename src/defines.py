#!/usr/bin/env python
# -*- coding: ascii -*-
"""defines.py - this file contains meta data and program parameters"""

# Meta data
__author__ = "Nicolai Spicher"
__credits__ = ["Nicolai Spicher", "Stefan Maderwald", "Markus Kukuk", "Mark E. Ladd"]
__license__ = "GPL v3"
__version__ = "v0.2-beta"
__maintainer__ = "Nicolai Spicher"
__email__ = "nicolai[dot]spicher[at]fh-dortmund[dot]de"
__status__ = "Beta"
__url__ = "https://github.com/nspi/vbcg"
__description__ = "real-time application for video-based estimation of the hearts activity"

# Indices of program settings
IDX_WEBCAM = 0
IDX_CAMERA = 1
IDX_ALGORITHM = 2
IDX_CURVES = 3
IDX_FRAMES = 4
IDX_FACE = 5
IDX_FPS = 6
IDX_COLORCHANNEL = 7

# Indices of algorithm parameters
IDX_ZERO_PADDING = 0
IDX_WIN_SIZE = 1
IDX_RUN_MAX = 2
IDX_MIN_TIME = 3

# Standard values of program settings
VAL_WEBCAM = 1
VAL_CAMERA = 1
VAL_ALGORITHM = 0
VAL_CURVES = 1
VAL_FRAMES = 0
VAL_FACE = 0
VAL_FPS = 25
VAL_COLORCHANNEL = 1

# Standard values of algorithm parameters
VAL_ZERO_PADDING = 1
VAL_WIN_SIZE = 9
VAL_RUN_MAX = 3
VAL_MIN_TIME = 0.5

# Labels of algorithms in GUI
LABEL_ALGORITHM_1 = "Estimate HR (BMT 2015)"
LABEL_ALGORITHM_2 = "Filter signal (ISMRM 2016)"
LABEL_ALGORITHM_3 = "Trigger MRI (ISMRM 2015)"
