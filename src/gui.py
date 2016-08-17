#!/usr/bin/env python
# gui.py - GUI management

from gui_statusbar import Statusbar
from gui_toolbarROI import ToolbarROI
from gui_toolbarButtons import ToolbarButtons
from gui_windowVideo import WindowVideo
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


# Create root widget
root = Tk.Tk()


class GUI:
    # This is the main class of the gui

    def setCamera(self, cam):
        # Register camera thread
        self.cameraThread = cam
        logging.info("Link to camera thread was stored in GUI class")

    def start(self):
        # Create gui

        MainWindow(root, self, self.cameraThread)
        logging.info('Main window was created')

        logging.info('Starting TkInter main loop')
        root.mainloop()


class MainWindow(Tk.Frame):
    # This class contains all GUI elements of the main window

    def __init__(self, parent, thread, cam):

        self.toolbar_roi = ToolbarROI(self, root)
        logging.info('Created toolbar for ROI definition')

        self.video_display = WindowVideo(self, root, thread, cam, self.toolbar_roi)
        logging.info('Created part of the GUI that shows video')

        self.statusbar = Statusbar(self, root, self.video_display)
        logging.info('Created status bar')

        self.signal_display = WindowSignal(self, thread, cam, self.statusbar)
        logging.info('Created part of the GUI that shows the signal extracted from the video')

        self.toolbar_buttons = ToolbarButtons(self, root, thread, cam, self.signal_display)
        logging.info('Created toolbar with buttons')


class WindowSignal(Tk.Frame):
    # In this frame the signal extracted from the video stream is shown
    # We have to keep it in this file because otherwise Tkinter throws an error
    # Todo: Find a more elegant solution

    def __init__(self, parent, thread, cam, statusbar):

        # Store camera object
        self.cameraInstance = cam

        # Store statusbar object
        self.statusbar = statusbar

        # Create GUI
        self.__create_gui()

    def __create_gui(self):
        self.figure = Mat_figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        # Call thread that displays signal
        self.signalPlotThread = SignalPlotter(self.cameraInstance, self.figure, self.canvas, self.subplot, self.statusbar)
        self.signalPlotThread.start()

    def closeSignalPlotterThread(self):
        self.signalPlotThread.closeSignalPlotterThread()


class SignalPlotter(threading.Thread):
    # This thread is used for continously plotting the mean signal of the video in the ROI

    def __init__(self, cam, figure, canvas, subplot, statusbar):

        # Store camera object
        self.cameraInstance = cam

        # Store figure, canvas, subplot
        self.figureInstance = figure
        self.canvasInstance = canvas
        self.subplotInstance = subplot
        self.statusbar = statusbar

        # Get current parameters
        self.curr_settings = settings.get_parameters()

        # Create empty vector for signal
        self.values = np.zeros((1, 1))

        # Update statusbar value
        self.statusbar.updateInfoText("Waiting for enough frames...")

        # Configure thread
        threading.Thread.__init__(self)
        self.eventProgramEnd = threading.Event()
        self.eventProgramEnd.clear()

    def closeSignalPlotterThread(self):
        # Activate event to end thread
        self.eventProgramEnd.set()

    def run(self):

        # run() method of cameraThread waits for shutdown event
        while self.eventProgramEnd.is_set() is False:

            # Get camera event
            self.cameraActive = self.cameraInstance.getEventCameraReady()

            # If camera is available, compute mean value and store it
            if self.cameraActive:

                # Get frame
                tmp, self.currentFrame = self.cameraInstance.getFrame()

                # Compute mean value
                self.mean_value = cv2.mean(self.currentFrame)[1]

                # Store mean value
                self.values = np.append(self.values, self.mean_value)

                # Begin with computations when 300 data points are accumulated
                if np.size(self.values) >= 300:

                    # Update statusbar value
                    self.statusbar.updateInfoText("Starting computation")

                    # Perform algorithms depending on user selection
                    if self.curr_settings[IDX_ALGORITHM] == 1:

                        # Normalize values
                        self.valuesNorm = signal_processing.normalize(self.values)
                        # Perform pseudo derivation
                        self.valuesNormDiff = np.abs(np.diff(self.valuesNorm))
                        # Get output
                        self.valuesOutput = self.valuesNormDiff

                    elif self.curr_settings[IDX_ALGORITHM] == 2:

                        # Todo: Implement algorithm #2

                        # Get output
                        self.valuesOutput = signal_processing.normalize(self.values)

                    else:

                        # Todo: Implement algorithm #3

                        # Get output
                        self.valuesOutput = signal_processing.normalize(self.values)


                    # Delete one data point to maintain 300 values
                    mask = np.ones(len(self.values), dtype=bool)
                    mask[0:np.size(self.values) - 300] = False
                    self.values = self.values[mask]

                else:
                    self.valuesOutput = signal_processing.normalize(self.values)

            # Show signal
            try:
                self.subplotInstance.clear()
                self.subplotInstance.plot(self.valuesOutput)
                self.canvasInstance.draw()
            except RuntimeError:
                # ''Quit'' button has been pressed by a user, resulting in RuntimeError during program shutdown
                # Todo: Find a more elegant solution
                logging.info("Signal plotting thread will be halted")

        logging.info("Reached of signal plotting thread")

