#!/usr/bin/env python
# gui.py - GUI management

from gui_statusbar import Statusbar
from gui_toolbarROI import ToolbarROI
from gui_toolbarButtons import ToolbarButtons
from gui_windowVideo import WindowVideo
from gui_windowSignal import WindowSignal

import Tkinter as Tk
import logging

# Create root widget
root = Tk.Tk()
# Set title in navigation bar
root.wm_title("vbcg")

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

        self.statusbar = Statusbar(self, root)
        logging.info('Created status bar')

        self.toolbar_roi = ToolbarROI(self, root)
        logging.info('Created toolbar for ROI definition')

        self.video_display = WindowVideo(self, root, thread, cam, self.toolbar_roi, self.statusbar)
        logging.info('Created part of the GUI that shows video')

        self.signal_display = WindowSignal(self, root, thread, cam, self.statusbar, self.video_display)
        logging.info('Created part of the GUI that shows the signal extracted from the video')

        self.toolbar_buttons = ToolbarButtons(self, root, thread, cam, self.signal_display)
        logging.info('Created toolbar with buttons')

