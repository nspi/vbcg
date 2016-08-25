#!/usr/bin/env python
# -*- coding: ascii -*-
"""gui_windowSignal.py - GUI element: frame that displays signal"""

from defines import  *

import Tkinter as Tk
import matplotlib
import logging
import threading
import numpy as np
import cv2
import signal_processing
import settings

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure as Mat_figure
matplotlib.use('TkAgg')


class WindowSignal(Tk.Frame):
    # In this frame the signal extracted from the video stream is shown

    def __init__(self, parent, tk_root, thread, cam, statusbar, video_display):

        global root
        self.root = tk_root

        # Store camera object
        self.cameraInstance = cam

        # Store statusbar object
        self.statusbar = statusbar

        # Store video display object
        self.video_display = video_display

        # Create GUI
        self.__create_gui()

    def __create_gui(self):

        # Add subplots
        self.figure = Mat_figure(figsize=(5, 4), dpi=100)
        self.subplotTop = self.figure.add_subplot(211)
        self.subplotBottom = self.figure.add_subplot(212)

        # Add labels
        self.subplotTop.set_xlabel('Frames')
        self.subplotBottom.set_xlabel('Hz')
        # Change font size
        matplotlib.rcParams.update({'font.size': 10})

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        # Call thread that displays signal
        self.signalPlotThread = SignalPlotter(self.root, self.cameraInstance, self.figure, self.canvas, self.subplotTop, self.subplotBottom, self.statusbar, self.video_display)
        self.signalPlotThread.start()

    def closeSignalPlotterThread(self):
        self.signalPlotThread.closeSignalPlotterThread()


class SignalPlotter(threading.Thread):
    # This thread is used for continously plotting the mean signal of the video in the ROI

    def __init__(self, tk_root, cam, figure, canvas, subplotTop, subplotBottom, statusbar, video_display):

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

        # Get current parameters
        self.settingsInstance = settings
        self.curr_settings = self.settingsInstance.get_parameters()

        # Create empty vector for signal
        self.valuesRaw = np.zeros((1, 1))
        self.valuesOutput =  np.zeros((300, 1))
        self.valuesOutput2 = np.zeros((300, 1))

        # Initialize variables for FPS computation
        self.frameCounter = 0
        self.frameCounterLastValue = 0

        # Start thread for FPS computation
        self.fpsCounterThread = threading.Thread(target=self.__computeFPS)
        self.fpsCounterThread.start()

        # Update statusbar value
        self.statusbarInstance.updateInfoText("Please choose a camera")

        # Configure thread
        threading.Thread.__init__(self)
        self.eventProgramEnd = threading.Event()
        self.eventProgramEnd.clear()

    def closeSignalPlotterThread(self):
        # Activate event to end thread
        self.eventProgramEnd.set()

    def run(self):

        # Variable for statusbar information
        self.enoughFrames = False

        # Set statusbar value
        self.statusbarInstance.setFPSCounter2(0)

        # run() method of cameraThread waits for shutdown event
        while self.eventProgramEnd.is_set() is False:

            # Get camera event
            self.cameraActive = self.cameraInstance.getEventCameraReady()

            # Get current options
            self.curr_settings = self.settingsInstance.get_parameters()

            # If camera is available, compute mean value and store it
            if self.cameraActive.is_set():

                # Update values in statusbar
                self.statusbarInstance.setFPSCounter2(self.FPS)

                # Update statusbar value if not enough frames available for computations
                if not self.enoughFrames:
                    self.statusbarInstance.updateInfoText("Waiting for enough frames")

                # Get frame
                tmp, self.currentFrame = self.cameraInstance.getFrame()

                # Compute mean value
                self.mean_value = cv2.mean(self.currentFrame)[1]

                # Store mean value
                self.valuesRaw = np.append(self.valuesRaw, self.mean_value)

                # Begin with computations when 300 data points are accumulated
                if np.size(self.valuesRaw) >= 300:

                    # Set variable
                    self.enoughFrames = True

                    # Update statusbar value
                    self.statusbarInstance.updateInfoText("Performing computations")

                    # Perform algorithms depending on user selection
                    if self.curr_settings[IDX_ALGORITHM] == 1:

                        # Compute algorithm
                        self.HR, self.spectrum, self.spectrumAxis, self.spectrumMax = signal_processing.computeHR(self.valuesRaw, self.FPS)
                        # Store heart rate value
                        self.HRstring = str(self.HR)
                        self.video_display.set_HeartRateText(self.HRstring[0:self.HRstring.find('.')])
                        # Normalize signals for display
                        self.valuesOutput = signal_processing.normalize(self.valuesRaw)
                        self.valuesOutput2 = signal_processing.normalize(self.spectrum)

                    elif self.curr_settings[IDX_ALGORITHM] == 2:

                        # Compute algorithm
                        self.valuesOutput2 = signal_processing.filterWaveform(self.valuesRaw,self.valuesOutput2,20)

                        # Normalize signals for display
                        self.valuesOutput = signal_processing.normalize(self.valuesRaw)
                        self.valuesOutput2 = signal_processing.normalize(self.valuesOutput2)

                    # Delete data points to maintain 300 values
                    mask = np.ones(len(self.valuesRaw), dtype=bool)
                    mask[0:np.size(self.valuesRaw) - 300] = False
                    self.valuesRaw = self.valuesRaw[mask]
                    self.valuesOutput = self.valuesOutput[mask]
                    if self.curr_settings[IDX_ALGORITHM] == 2:
                        self.valuesOutput2 = self.valuesOutput2[mask]

                else:
                    self.valuesOutput = signal_processing.normalize(self.valuesRaw)

            # Increase counter
            self.frameCounter += 1

            try:
                # If camera available and the user enabled the option, plot signal
                if self.cameraActive.is_set() and self.curr_settings[IDX_CURVES]:

                    # Clear subplot
                    self.subplotInstanceTop.clear()
                    self.subplotInstanceBottom.clear()

                    # Plot results based on algorithm
                    if self.curr_settings[IDX_ALGORITHM] == 1:

                        self.subplotInstanceTop.plot(self.valuesOutput)
                        self.subplotInstanceTop.legend(["Average video signal in ROI"], fontsize=9)
                        self.subplotInstanceTop.set_xlabel('Frames')

                        # Plot spectrum if it is available, i.e. the algorithm has been computed once
                        if  (np.count_nonzero(self.valuesOutput2)>=1):

                            self.subplotInstanceBottom.plot(self.spectrumAxis,self.valuesOutput2)
                            self.subplotInstanceBottom.plot(self.spectrumAxis[self.spectrumMax], self.valuesOutput2[self.spectrumMax],'r*')
                            self.subplotInstanceBottom.legend(["One-sided Amplitude spectrum"], fontsize=9)
                            self.subplotInstanceBottom.set_xlabel('Hz')


                    elif self.curr_settings[IDX_ALGORITHM] == 2:

                        self.subplotInstanceTop.plot(self.valuesOutput)
                        self.subplotInstanceTop.legend(["Average video signal in ROI"], fontsize=9)
                        self.subplotInstanceTop.set_xlabel('Frames')

                        # Plot spectrum if it is available, i.e. the algorithm has been computed once
                        if  (np.count_nonzero(self.valuesOutput2)>=1):

                            self.subplotInstanceBottom.plot(self.valuesOutput2)
                            self.subplotInstanceBottom.legend(["Filtered waveform"], fontsize=9)
                            self.subplotInstanceBottom.set_xlabel('Frames')

                # Draw to canvas
                self.canvasInstance.draw()

            except RuntimeError:
                # ''Quit'' button has been pressed by a user, resulting in RuntimeError during program shutdown
                # Todo: Find a more elegant solution
                logging.info("Signal plotting thread will be halted")

        logging.info("Reached of signal plotting thread")


    def __computeFPS(self):

                # Compute FPS
                self.FPS = self.frameCounter - self.frameCounterLastValue

                # Update value
                self.frameCounterLastValue = self.frameCounter

                # Restart
                self.root.after(1000, lambda: self.__computeFPS())


    def get_frameCounter(self):
        return self.frameCounter