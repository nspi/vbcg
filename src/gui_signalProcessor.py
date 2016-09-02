#!/usr/bin/env python
# -*- coding: ascii -*-
"""gui_signalProcessor.py - Thread for processing the signal from the video"""

from defines import *
from signal_processing import SignalProcessor

import logging
import threading
import numpy as np
import cv2
import settings
import datetime


class GuiSignalProcessor(threading.Thread):
    """This thread is used for continously plotting the mean signal of the video in the ROI"""

    def __init__(self, tk_root, cam, figure, canvas, subplotTop, subplotBottom, statusbar,
                 video_display, frameQueuePlot):
        """Initializes variables etc"""

        # Store camera object
        self.cameraInstance = cam

        # Store root object
        self.root = tk_root

        # Store figure, canvas, subplot, video_display
        self.figureInstance = figure
        self.canvasInstance = canvas
        self.subplotInstanceTop = subplotTop
        self.subplotInstanceBottom = subplotBottom
        self.statusbarInstance = statusbar
        self.video_display = video_display

        # Store frame queue
        self.frameQueue = frameQueuePlot

        # Create signal processing object
        self.signalProcessingInstance = SignalProcessor()

        # Get current parameters
        self.settingsInstance = settings
        self.curr_settings = self.settingsInstance.get_parameters()

        # Fix FPS and length of shown signal
        self.FPS = self.curr_settings[IDX_FPS]
        self.lengthSignal = 500

        # Temporary variable
        self.firstRun = True

        # Initialize variables that will contain results later
        self.valuesRaw = np.zeros((self.lengthSignal, 1))            # Raw signal from video
        self.valuesOutput = np.zeros((self.lengthSignal, 1))         # Filtered signal for top plot
        self.valuesOutput2 = np.zeros((self.lengthSignal, 1))        # Filtered signal for bottom plot
        self.spectrumAxis = np.zeros((self.lengthSignal, 1))         # For HR algorithm only: Axis of spectrum
        self.spectrumMax = 1                                         # For HR algorithm only: Estimated Heart Rate

        # Update statusbar value
        self.statusbarInstance.updateInfoText("Please choose a camera")

        # Configure iself as thread
        threading.Thread.__init__(self)
        self.eventProgramEnd = threading.Event()
        self.eventProgramEnd.clear()

    def closeSignalPlotterThread(self):
        """Activate event to end thread"""
        self.eventProgramEnd.set()

    def __waitToAdjustFPS(self, startTime, endTime):
        # Compute difference to desired FPS
        self.diffTime = (endTime - startTime).total_seconds()
        self.waitTime = 1.0 / self.FPS - self.diffTime

        # Wait the remaining to reach desired FPS
        if int(self.waitTime*1000) > 0:
            cv2.waitKey(int(self.waitTime * 1000))
        elif int(self.waitTime*1000) == 0:
            cv2.waitKey(33) # cv2.waitKey(0) results in error


    def run(self):
        """The main functionality of the thread: The signal is obtained and plotted"""

        # run() method of cameraThread waits for shutdown event
        while self.eventProgramEnd.is_set() is False:

            # Get time
            self.startTime = datetime.datetime.now()

            # Get frame
            realFramesAvailable, self.currentFrame = self.cameraInstance.getFrame()

            # If real frames are available, start main activity
            if realFramesAvailable is True:

                if self.firstRun is True:

                    # Update statusbar value
                    self.statusbarInstance.updateInfoText("Processing frames")

                    # Get current settings
                    self.curr_settings = self.settingsInstance.get_parameters()

                    # Update FPS
                    self.FPS = self.curr_settings[IDX_FPS]
                    self.colorChannel = int(self.curr_settings[IDX_COLORCHANNEL])

                    self.firstRun = False

                # Compute mean value
                self.mean_value = cv2.mean(self.currentFrame)[self.colorChannel]

                # Store mean value
                self.valuesRaw = np.append(self.valuesRaw, self.mean_value)

                # Begin with computations when enough data points are accumulated
                if np.size(self.valuesRaw) >= self.lengthSignal:

                    # Perform algorithms depending on user selection
                    if self.curr_settings[IDX_ALGORITHM] == 0:

                        # Compute algorithm
                        self.HR, self.spectrum, self.spectrumAxis, self.spectrumMax = \
                            self.signalProcessingInstance.computeHR(self.valuesRaw, self.FPS)

                        # Store heart rate value
                        self.HRstring = str(self.HR)
                        self.video_display.set_HeartRateText(self.HRstring[0:self.HRstring.find('.')])

                        # Normalize signals for display
                        self.valuesOutput = self.signalProcessingInstance.normalize(self.valuesRaw)
                        self.valuesOutput2 = self.signalProcessingInstance.normalize(self.spectrum)

                    elif self.curr_settings[IDX_ALGORITHM] == 1:

                        # Compute algorithm
                        self.boolTrigger, self.valuesFiltered = \
                            self.signalProcessingInstance.filterWaveform(self.valuesRaw, self.valuesOutput2, 9, 3, 0.5)

                        # Send trigger
                        if self.boolTrigger is True:
                            self.video_display.displayHeartTrigger()

                        # Normalize signals for display
                        self.valuesOutput = self.signalProcessingInstance.normalize(self.valuesRaw)
                        self.valuesOutput2 = self.valuesFiltered

                    # Delete data points to maintain self.lengthSignal values
                    mask = np.ones(len(self.valuesRaw), dtype=bool)
                    mask[0:np.size(self.valuesRaw) - self.lengthSignal] = False
                    self.valuesRaw = self.valuesRaw[mask]
                    self.valuesOutput = self.valuesOutput[mask]
                    if self.curr_settings[IDX_ALGORITHM] == 1:
                        self.valuesOutput2 = self.valuesOutput2[mask]

            # Store data in dictionary
            if self.curr_settings[IDX_ALGORITHM] == 0:
                self.dict = {'valuesOutput': self.valuesOutput, 'valuesOutput2': self.valuesOutput2,
                             'spectrumAxis': self.spectrumAxis, 'spectrumMax': self.spectrumMax}
            elif self.curr_settings[IDX_ALGORITHM] == 1:
                self.dict = {'valuesOutput': self.valuesOutput, 'valuesOutput2': self.valuesOutput2}

            # Put dictionary in queue
            self.frameQueue.put(self.dict)

            # Wait and start from beginning of thread
            self.__waitToAdjustFPS(self.startTime, datetime.datetime.now())

        logging.info("Reached end of signal processing thread")
