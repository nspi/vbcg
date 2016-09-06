#!/usr/bin/env python
# -*- coding: ascii -*-
"""gui_windowSignal.py - GUI element: frame that displays signal"""

import Tkinter as Tk
import matplotlib

from Queue import LifoQueue
from gui_signalPlotter import GuiSignalPlotter
from gui_signalProcessor import GuiSignalProcessor
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure as Mat_figure
matplotlib.use('Tkagg')


class WindowSignal(Tk.Frame):
    """In this frame the signal extracted from the video stream is shown"""

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
        self.figure = Mat_figure(figsize=(5, 3), dpi=100)
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

        # We store the data that is interchanged from GuiSignalProcessor to GuiSignalPlotter in a queue
        self.dataQueue = LifoQueue()

        # Create thread that displays signal
        self.signalPlotThread = GuiSignalPlotter(self.root, self.cameraInstance, self.figure, self.canvas,
                                                 self.subplotTop, self.subplotBottom, self.statusbar,
                                                 self.video_display, self.dataQueue)
        # Create thread that processes signal
        self.signalProcessorThread = GuiSignalProcessor(self.root, self.cameraInstance, self.figure, self.canvas,
                                                        self.subplotTop, self.subplotBottom, self.statusbar,
                                                        self.video_display, self.dataQueue)

        # Start both threads
        self.signalPlotThread.start()
        self.signalProcessorThread.start()

    def closeThreads(self):
        """Closes signal plotting and processing threads"""
        self.signalPlotThread.closeSignalPlotterThread()
        self.signalProcessorThread.closeSignalPlotterThread()
