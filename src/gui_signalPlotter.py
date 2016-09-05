#!/usr/bin/env python
# -*- coding: ascii -*-
"""gui_signalPlotter.py - Thread for plotting the signal from the video"""

from defines import *

import logging
import threading
import numpy as np
import settings
import datetime


class GuiSignalPlotter(threading.Thread):
    """This thread is used for continously plotting the signal in the ROI"""

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

        # Get current settings instance
        self.settingsInstance = settings

        # Configure itself as thread
        threading.Thread.__init__(self)
        self.eventProgramEnd = threading.Event()
        self.eventProgramEnd.clear()

    def closeSignalPlotterThread(self):
        """Activate event to end thread"""
        self.eventProgramEnd.set()

    def run(self):
        """The main functionality of the thread: The signal is obtained and plotted as fast as possible (no waiting)"""

        # Todo: Fix rare error:
        # self.spectrumAxis = self.dict['spectrumAxis']
        # KeyError: 'spectrumAxis'

        # run() method of cameraThread waits for shutdown event
        while self.eventProgramEnd.is_set() is False:

            # Get time
            self.startTime = datetime.datetime.now()

            # Get camera event
            self.cameraActive = self.cameraInstance.getEventCameraReady()

            # Get current options
            self.curr_settings = self.settingsInstance.get_parameters()

            # Get dictionary from queue
            if self.frameQueue.empty() is False:

                self.dict = self.frameQueue.get()

                # Get data from dictionary
                if self.curr_settings[IDX_ALGORITHM] == 0:
                    try:
                        self.valuesOutput = self.dict['valuesOutput']
                        self.valuesOutput2 = self.dict['valuesOutput2']
                        self.spectrumAxis = self.dict['spectrumAxis']
                        self.spectrumMax = self.dict['spectrumMax']
                    except KeyError:
                        # just to be safe if the algorithm has been changed since initialization of self.curr_settings
                        self.valuesOutput = self.dict['valuesOutput']
                        self.valuesOutput2 = self.dict['valuesOutput2']

                elif self.curr_settings[IDX_ALGORITHM] == 1:
                    self.valuesOutput = self.dict['valuesOutput']
                    self.valuesOutput2 = self.dict['valuesOutput2']

                try:

                    # If camera available and the user enabled the option, plot signal
                    if self.cameraActive.is_set() and self.curr_settings[IDX_CURVES]:

                        # Clear subplot
                        self.subplotInstanceTop.clear()
                        self.subplotInstanceBottom.clear()

                        # Plot results based on algorithm
                        if self.curr_settings[IDX_ALGORITHM] == 0:

                            self.subplotInstanceTop.plot(self.valuesOutput)
                            self.subplotInstanceTop.legend(["Average video signal in ROI"], fontsize=9)

                            # Plot spectrum if it is available, i.e. the algorithm has been computed once
                            if np.count_nonzero(self.valuesOutput2) >= 1:
                                self.subplotInstanceBottom.plot(self.spectrumAxis, self.valuesOutput2)
                                self.subplotInstanceBottom.plot(self.spectrumAxis[self.spectrumMax],
                                                                self.valuesOutput2[self.spectrumMax], 'r*')
                            # Otherwise, plot placeholder
                            else:
                                self.subplotInstanceBottom.plot(self.valuesOutput2)

                            self.subplotInstanceBottom.legend(["One-sided Amplitude spectrum",
                                                               "Maximum value"], fontsize=9)
                            self.subplotInstanceBottom.set_xlabel('Hz')

                        elif self.curr_settings[IDX_ALGORITHM] == 1:

                            self.subplotInstanceTop.plot(self.valuesOutput)
                            self.subplotInstanceTop.legend(["Average video signal in ROI"], fontsize=9)

                            # Plot filtered signal if it is available, i.e. the algorithm has been computed once
                            if np.count_nonzero(self.valuesOutput2) >= 1:
                                self.subplotInstanceBottom.plot(self.valuesOutput2)
                                self.subplotInstanceBottom.legend(["Filtered waveform"], fontsize=9)
                                self.subplotInstanceBottom.set_xlabel('Frames')

                    else:
                        # Needed for windows implementation, otherwise the whole GUI stays blank
                        self.subplotInstanceTop.clear()
                        self.subplotInstanceBottom.clear()

                except RuntimeError:
                    # ''Quit'' button has been pressed by a user, resulting in RuntimeError during program shutdown
                    logging.info("Signal plotting thread will be halted")

                # Draw canvas
                self.canvasInstance.draw()

        logging.info("Reached end of signal plotting thread")
