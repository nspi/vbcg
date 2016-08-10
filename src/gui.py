#!/usr/bin/env python
# gui.py - GUI management

import Tkinter as Tk
import matplotlib
import logging

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure as Mat_figure
matplotlib.use('TkAgg')

from gui_statusbar import Statusbar
from gui_toolbarROI import ToolbarROI
from gui_toolbarButtons import ToolbarButtons
from gui_windowVideo import WindowVideo

# Create root widget
root = Tk.Tk()


class WindowSignal(Tk.Frame):
    # In this frame the signal extracted from the video stream is shown
    # We have to keep it in this file because otherwise Tkinter throws an error

    def __init__(self, parent, *args, **kwargs):
        # Create GUI
        self.__create_gui()

    def __create_gui(self):
        figure = Mat_figure(figsize=(5, 4), dpi=100)
        figure.add_subplot(111)

        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.show()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


class MainWindow(Tk.Frame):
    # This class contains all GUI elements of the main window

    def __init__(self, parent, thread, cam):

        Tk.Frame.__init__(self, parent)

        self.video_display = WindowVideo(self,root,thread,cam)
        logging.info('Created part of the GUI that shows video')

        self.signal_display = WindowSignal(self)
        logging.info('Created part of the GUI that shows the signal extracted from the video')

        self.statusbar = Statusbar(self, root, self.video_display)
        logging.info('Created status bar')

        self.toolbar_roi = ToolbarROI(self, root)
        logging.info('Created toolbar for ROI definition')

        self.toolbar_buttons = ToolbarButtons(self, root, thread, cam)
        logging.info('Created toolbar with buttons')


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
