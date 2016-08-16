#!/usr/bin/env python
# gui.py - GUI management

import Tkinter as Tk
import matplotlib
import logging
import threading

import numpy as np
import cv2

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure as Mat_figure
matplotlib.use('TkAgg')

from gui_statusbar import Statusbar
from gui_toolbarROI import ToolbarROI
from gui_toolbarButtons import ToolbarButtons
from gui_windowVideo import WindowVideo

# Create root widget
root = Tk.Tk()



class GUI():
    # This is the main class of gui

    def setCamera(self,cam):
        # Register camera thread

        global cameraThread
        self.cameraThread = cam
        logging.info("Link to camera thread was stored in GUI class")

    def start(self):
        # Create gui

        MainWindow(root,self,self.cameraThread)
        logging.info('Main window was created')

        logging.info('Starting TkInter main loop')
        root.mainloop()


class MainWindow(Tk.Frame):
    # This class contains all GUI elements of the main window

    def __init__(self, parent, thread, cam):

        Tk.Frame.__init__(self, parent)

        self.toolbar_roi = ToolbarROI(self, root)
        logging.info('Created toolbar for ROI definition')

        self.video_display = WindowVideo(self, root, thread, cam, self.toolbar_roi)
        logging.info('Created part of the GUI that shows video')

        self.signal_display = WindowSignal(self, thread, cam)
        logging.info('Created part of the GUI that shows the signal extracted from the video')

        self.statusbar = Statusbar(self, root, self.video_display)
        logging.info('Created status bar')

        self.toolbar_buttons = ToolbarButtons(self, root, thread, cam, self.signal_display)
        logging.info('Created toolbar with buttons')



class WindowSignal(Tk.Frame):
    # In this frame the signal extracted from the video stream is shown
    # We have to keep it in this file because otherwise Tkinter throws an error


    def __init__(self, parent, thread, cam):

        # Store camera object
        self.cameraInstance = cam

        # Create GUI
        self.__create_gui()

    def __create_gui(self):
        self.figure = Mat_figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        # Call thread that displays signal
        self.stopFlag = threading.Event()
        self.signalPlotThread = SignalPlotter(self.stopFlag, self.cameraInstance, self.figure, self.canvas, self.subplot)
        self.signalPlotThread.start()

    def getEvent(self):
        return self.stopFlag


class SignalPlotter(threading.Thread):
    # This thread is used for continously plotting the mean signal of the video in the ROI

    def __init__(self, event, cam, figure, canvas, subplot):

        # Store camera object
        self.cameraInstance = cam

        # Store figure, canvas, subplot
        self.figureInstance = figure
        self.canvasInstance = canvas
        self.subplotInstance = subplot

        # Create empty vector for signal
        self.values = np.zeros((1, 1))

        # Configure thread
        threading.Thread.__init__(self)
        self.stopFlag = event

    def run(self):

        # run() method of cameraThread waits for shutdown event
        while self.stopFlag.is_set() is False:

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
                # Remove value if array reached 300 values
                if np.size(self.values) >= 30:
                    mask = np.ones(len(self.values), dtype=bool)
                    mask[0:np.size(self.values) - 30] = False
                    self.values = self.values[mask]

                # Show signal
                self.subplotInstance.clear()
                self.subplotInstance.plot(self.values)
                self.canvasInstance.draw()

        print 1
        # todo: find out why we do not reach this line. Maybe because canvas is not available anymore?
        logging.info("Signal plotting thread will be halted")
