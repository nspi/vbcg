#!/usr/bin/env python
# -*- coding: ascii -*-
"""gui.py - the main GUI class that contains all GUI elements"""

from gui_statusbar import Statusbar
from gui_toolbarROI import ToolbarROI
from gui_toolbarButtons import ToolbarButtons
from gui_windowVideo import WindowVideo
from gui_windowSignal import WindowSignal
from defines import programVersion

import Tkinter as Tk
import logging

# Create root widget
root = Tk.Tk()

# Set title in navigation bar
root.wm_title("vbcg " + str(programVersion))


class GUI(object):
    """This is the main class of the gui. Here, we use Tkinter for thread management"""

    def setVideoThread(self, videoThread):
        """Register camera thread"""
        self.cameraThread = videoThread
        logging.info("Link to thread that delivers video frames was stored in GUI thread")

    def start(self):
        """Create GUI"""
        MainWindow(self, self.cameraThread)
        logging.info('Main window was created')

        # Start Tkinter thread
        logging.info('Starting TkInter main loop')
        root.mainloop()


class MainWindow(object):
    """This class contains all GUI elements of the main window"""

    def __init__(self, GUI_thread, videoThread):

        self.statusbar = Statusbar(self, root)
        logging.info('Created status bar')

        self.toolbar_roi = ToolbarROI(self, root)
        logging.info('Created toolbar for ROI definition')

        self.video_display = WindowVideo(self, root, GUI_thread, videoThread, self.toolbar_roi, self.statusbar)
        logging.info('Created part of the GUI that shows video')

        self.signal_display = WindowSignal(self, root, GUI_thread, videoThread, self.statusbar, self.video_display)
        logging.info('Created part of the GUI that shows the signal extracted from the video')

        self.toolbar_buttons = ToolbarButtons(self, root, GUI_thread, videoThread, self.signal_display)
        logging.info('Created toolbar with buttons')
