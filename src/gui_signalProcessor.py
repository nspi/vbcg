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
    """This thread is used for continuously plotting the mean signal of the video in the ROI"""

    def __init__(self, tk_root, cam, figure, canvas, subplot_top, subplot_bottom, statusbar,
                 video_display, frame_queue):
        """Initializes variables etc"""

        # Store camera object
        self.cameraInstance = cam

        # Store root object
        self.root = tk_root

        # Store figure, canvas, subplot, video_display
        self.figureInstance = figure
        self.canvasInstance = canvas
        self.subplotInstanceTop = subplot_top
        self.subplotInstanceBottom = subplot_bottom
        self.statusbarInstance = statusbar
        self.video_display = video_display

        # Store frame queue
        self.frameQueue = frame_queue

        # Initialize variables
        self.startTime = self.cameraActive = self.currSettings = self.dict = self.spectrumAxis = \
            self.spectrumMax = self.valuesOutput = self.valuesOutput2 = self.realFramesAvailable =\
            self.currentFrame = self.colorChannel = self.mean_value = self.HR = self.HRstring =\
            self.spectrum = self.show_trigger_symbol = self.valuesFiltered = None

        # Create signal processing object
        self.signalProcessingInstance = SignalProcessor()

        # Get current parameters
        self.settingsInstance = settings
        self.currSettings = self.settingsInstance.get_parameters()

        # Fix FPS and length of shown signal
        self.FPS = self.currSettings[IDX_FPS]
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
        self.statusbarInstance.update_info_text("Please choose a camera or folder containing frames")

        # Configure itself as thread
        threading.Thread.__init__(self)
        self.eventProgramEnd = threading.Event()
        self.eventProgramEnd.clear()

    def close_signal_processor_thread(self):
        """Activate event to end thread"""
        self.signalProcessingInstance.clear()
        self.eventProgramEnd.set()

    def __wait_to_adjust_fps(self, start_time, end_time):
        # Compute difference to desired FPS
        self.diffTime = (end_time - start_time).total_seconds()
        self.waitTime = 1.0 / self.FPS - self.diffTime

        # Wait the remaining to reach desired FPS
        if int(self.waitTime * 1000) > 0:
            cv2.waitKey(int(self.waitTime * 1000))
        elif int(self.waitTime * 1000) == 0:
            cv2.waitKey(33)  # cv2.waitKey(0) results in error

    def run(self):
        """The main functionality of the thread: The signal is obtained and plotted"""

        # run() method of cameraThread waits for shutdown event
        while self.eventProgramEnd.is_set() is False:

            # Get time
            self.startTime = datetime.datetime.now()

            # Get frame
            self.realFramesAvailable, self.currentFrame = self.cameraInstance.get_frame()

            # If real frames are available, start main activity
            if self.realFramesAvailable is True:

                # Get current settings
                self.currSettings = self.settingsInstance.get_parameters()

                if self.firstRun is True:

                    # Update statusbar value
                    self.statusbarInstance.update_info_text("Processing frames")

                    # Update FPS
                    self.FPS = self.currSettings[IDX_FPS]
                    self.colorChannel = int(self.currSettings[IDX_COLORCHANNEL])

                    self.firstRun = False

                # Compute mean value
                self.mean_value = cv2.mean(self.currentFrame)[self.colorChannel]

                # Store mean value
                self.valuesRaw = np.append(self.valuesRaw, self.mean_value)

                # Begin with computations when enough data points are accumulated
                if np.size(self.valuesRaw) >= self.lengthSignal:

                    # Perform algorithms depending on user selection
                    if self.currSettings[IDX_ALGORITHM] == 0:

                        # Compute algorithm
                        self.HR, self.spectrum, self.spectrumAxis, self.spectrumMax = \
                            self.signalProcessingInstance.compute_heart_rate(self.valuesRaw, self.FPS)

                        # Store heart rate value
                        self.HRstring = str(self.HR)
                        self.video_display.set_heart_rate_text(self.HRstring[0:self.HRstring.find('.')])

                        # Normalize signals for display
                        self.valuesOutput = self.signalProcessingInstance.normalize(self.valuesRaw)
                        self.valuesOutput2 = self.signalProcessingInstance.normalize(self.spectrum)

                    elif self.currSettings[IDX_ALGORITHM] == 1:

                        # Compute algorithm
                        self.show_trigger_symbol, self.valuesFiltered = \
                            self.signalProcessingInstance.filter_waveform(self.valuesRaw, self.valuesOutput2, 9, 3, 0.5)

                        # Show symbol
                        if self.show_trigger_symbol is True:
                            self.video_display.display_heart_trigger()

                        # Normalize signals for display
                        self.valuesOutput = self.signalProcessingInstance.normalize(self.valuesRaw)
                        self.valuesOutput2 = self.valuesFiltered

                    elif self.currSettings[IDX_ALGORITHM] == 2:

                        # Compute algorithm
                        self.HR, self.spectrum, self.spectrumAxis, self.spectrumMax, self.triggerTimes =\
                            self.signalProcessingInstance.estimate_trigger(self.valuesRaw, self.FPS)

                        # Store heart rate value
                        self.HRstring = str(self.HR)
                        self.video_display.set_heart_rate_text(self.HRstring[0:self.HRstring.find('.')])

                        # Normalize signals for display
                        self.valuesOutput = self.signalProcessingInstance.normalize(self.valuesRaw)
                        self.valuesOutput2 = self.signalProcessingInstance.normalize(self.spectrum)

                    # Delete data points to maintain self.lengthSignal values
                    mask = np.ones(len(self.valuesRaw), dtype=bool)
                    mask[0:np.size(self.valuesRaw) - self.lengthSignal] = False
                    self.valuesRaw = self.valuesRaw[mask]
                    self.valuesOutput = self.valuesOutput[mask]
                    if self.currSettings[IDX_ALGORITHM] == 1:
                        self.valuesOutput2 = self.valuesOutput2[mask]

                # Store data in dictionary
                if self.currSettings[IDX_ALGORITHM] == 0:
                    self.dict = {'valuesOutput': self.valuesOutput, 'valuesOutput2': self.valuesOutput2,
                                 'spectrumAxis': self.spectrumAxis, 'spectrumMax': self.spectrumMax}
                elif self.currSettings[IDX_ALGORITHM] == 1:
                    self.dict = {'valuesOutput': self.valuesOutput, 'valuesOutput2': self.valuesOutput2}
                elif self.currSettings[IDX_ALGORITHM] == 2:
                    self.dict = {'valuesOutput': self.valuesOutput, 'valuesOutput2': self.valuesOutput2,
                                 'spectrumAxis': self.spectrumAxis, 'spectrumMax': self.spectrumMax,
                                 'triggerTimes': self.triggerTimes}
                # Put dictionary in queue
                self.frameQueue.put(self.dict)

            # Wait and start from beginning of thread
            self.__wait_to_adjust_fps(self.startTime, datetime.datetime.now())

        logging.info("Reached end of signal processing thread")
