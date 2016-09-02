#!/usr/bin/env python
# -*- coding: ascii -*-
"""gui_toolbarROI.py - GUI element: toolbar with textboxes for ROI definition"""

import Tkinter as Tk
import settings
import logging
import threading

from defines import *

# Initialize global variables
root = None


class ToolbarROI(Tk.Frame):
    """This toolbar allows to adjust the region-of-interest (ROI)"""

    def __init__(self, parent, tk_root):

        # Store variables
        global root
        self.root = tk_root
        self.x_min = self.x_max = self.y_min = self.y_max = 0

        # Initialize buttons
        self.textbox_x1 = self.textbox_x2 = self.textbox_y1 = self.textbox_y2 = None

        # Create GUI
        self.__createGUI()

        # Start thread that stores ROI
        self.storeROIThread = threading.Thread(target=self.__storeROI)
        self.storeColorThread = threading.Thread(target=self.__storeColorChannel)
        self.storeROIThread.start()
        self.storeColorThread.start()

    def __createGUI(self):
        """Create GUI elements and add them to root widget"""

        # Create frame that contains all folloowing elements
        self.button_frame = Tk.Frame(root, width=500, height=100)
        self.button_frame.pack(side=Tk.BOTTOM)

        # Add Checkbutton to decide whether to use Viola-Jones algorithm or manual ROI definition
        curr_settings = settings.get_parameters()
        self.check_button_1 = Tk.Checkbutton(master=self.button_frame, text="Face Detection",
                                             command=lambda: self.__violaJones())
        self.check_button_1.pack(side=Tk.LEFT)

        # Add empty box
        # Todo: use a dynamic solution
        self.label_x0 = Tk.Label(self.button_frame, text="  ")
        self.label_x0.pack(side=Tk.LEFT)

        # Fill list with available cameras and add to menu
        self.label_color_channels = Tk.Label(self.button_frame, text="Color channel:")
        self.label_color_channels.pack(side=Tk.LEFT)
        list_color_channels = ['']
        list_color_channels.append('R')
        list_color_channels.append('G')
        list_color_channels.append('B')
        list_color_channels.pop(0)
        self.list_color_channelsStr = Tk.StringVar()
        self.dropDownListColorChannel = Tk.OptionMenu(self.button_frame, self.list_color_channelsStr, *list_color_channels)
        self.list_color_channelsStr.set(list_color_channels[0])
        self.dropDownListColorChannel.pack(side=Tk.LEFT)

        # Add Textboxes for ROI definition
        self.label_x1 = Tk.Label(self.button_frame, text="X Begin:")
        self.label_x1.pack(side=Tk.LEFT)
        self.textbox_x1 = Tk.Text(self.button_frame, width=10, height=1)
        self.textbox_x1.pack(side=Tk.LEFT)
        self.textbox_x1.insert(Tk.END, self.x_min)

        self.label_x2 = Tk.Label(self.button_frame, text="X End:")
        self.label_x2.pack(side=Tk.LEFT)
        self.textbox_x2 = Tk.Text(self.button_frame, width=10, height=1)
        self.textbox_x2.pack(side=Tk.LEFT)
        self.textbox_x2.insert(Tk.END, self.x_max)

        self.label_y1 = Tk.Label(self.button_frame, text="Y Begin:")
        self.label_y1.pack(side=Tk.LEFT)
        self.textbox_y1 = Tk.Text(self.button_frame, width=10, height=1)
        self.textbox_y1.pack(side=Tk.LEFT)
        self.textbox_y1.insert(Tk.END, self.y_min)

        self.label_y2 = Tk.Label(self.button_frame, text="Y End:")
        self.label_y2.pack(side=Tk.LEFT)
        self.textbox_y2 = Tk.Text(self.button_frame, width=10, height=1)
        self.textbox_y2.pack(side=Tk.LEFT)
        self.textbox_y2.insert(Tk.END, self.y_max)

        # Disable Textboxes when Viola-Jones algorithm is active
        if curr_settings[IDX_FACE]:
            self.check_button_1.toggle()
            self.textbox_x1.config(bg='lightgray')
            self.textbox_x2.config(bg='lightgray')
            self.textbox_y1.config(bg='lightgray')
            self.textbox_y2.config(bg='lightgray')

    def __violaJones(self):
        """Action to perform when Viola-Jones button is pressed"""

        # Get current parameters
        settings.flip_parameter(IDX_FACE)
        curr_settings = settings.get_parameters()

        if curr_settings[IDX_FACE]:
            self.textbox_x1.config(bg='lightgray')
            self.textbox_x2.config(bg='lightgray')
            self.textbox_y1.config(bg='lightgray')
            self.textbox_y2.config(bg='lightgray')
            logging.info('Viola-Jones algorithm was activated by the user')
        else:
            self.textbox_x1.config(bg='white')
            self.textbox_x2.config(bg='white')
            self.textbox_y1.config(bg='white')
            self.textbox_y2.config(bg='white')
            logging.info('Viola-Jones algorithm was disabled by the user')

    def __storeColorChannel(self):
        """ Stores the desired color channel that is used for signal processing"""

        chan = self.list_color_channelsStr.get()

        if chan == "R":
            settings.change_parameter(IDX_COLORCHANNEL, 0)
        elif chan == "G":
            settings.change_parameter(IDX_COLORCHANNEL, 1)
        else:
            settings.change_parameter(IDX_COLORCHANNEL, 2)

        self.button_frame.after(1000, lambda: self.__storeColorChannel())

    def __storeROI(self):
        """Store ROI values from textboxes when it has more than 1 symbol and it contains of numbers only"""

        # Get values from textboxes
        if len(self.textbox_x1.get("1.0", Tk.END + "-1c")) > 0 & (
            self.textbox_x1.get("1.0", Tk.END + "-1c").isdigit() == len(self.textbox_x1.get("1.0", Tk.END + "-1c"))):
            self.x_min = int(self.textbox_x1.get("1.0", Tk.END + "-1c"))

        if len(self.textbox_x2.get("1.0", Tk.END + "-1c")) > 0 & (
            self.textbox_x2.get("1.0", Tk.END + "-1c").isdigit() == len(self.textbox_x2.get("1.0", Tk.END + "-1c"))):
            self.x_max = int(self.textbox_x2.get("1.0", Tk.END + "-1c"))

        if len(self.textbox_y1.get("1.0", Tk.END + "-1c")) > 0 & (
            self.textbox_y1.get("1.0", Tk.END + "-1c").isdigit() == len(self.textbox_y1.get("1.0", Tk.END + "-1c"))):
            self.y_min = int(self.textbox_y1.get("1.0", Tk.END + "-1c"))

        if len(self.textbox_y2.get("1.0", Tk.END + "-1c")) > 0 & (
            self.textbox_y2.get("1.0", Tk.END + "-1c").isdigit() == len(self.textbox_y2.get("1.0", Tk.END + "-1c"))):
            self.y_max = int(self.textbox_y2.get("1.0", Tk.END + "-1c"))

        # If *_min < *_max: Correct values
        if self.x_min > self.x_max:
            self.x_min = 0
            self.textbox_x1.delete(1.0, Tk.END)
            self.textbox_x1.insert(Tk.END, 0)
            logging.warn("Your ROI definition was inadequate (x_min < x_max). The values were corrected.")

        if self.y_min > self.y_max:
            self.y_min = 0
            self.textbox_y1.delete(1.0, Tk.END)
            self.textbox_y1.insert(Tk.END, 0)
            logging.warn("Your ROI definition was inadequate (y_min < y_max). The values were corrected.")

        # Repeat thread
        self.button_frame.after(1000, lambda: self.__storeROI())

    # Setter and getter following

    def disableRGBselection(self):
        self.dropDownListColorChannel.config(state=Tk.DISABLED)

    def getROI(self):
        """Returns current ROI definition"""
        return self.x_min, self.x_max, self.y_min, self.y_max

    def setROI(self, x_min, x_max, y_min, y_max):
        """Sets ROI to new defintion"""
        self.x_min = x_min
        self.textbox_x1.delete(1.0, Tk.END)
        self.textbox_x1.insert(Tk.END, self.x_min)

        self.x_max = x_max
        self.textbox_x2.delete(1.0, Tk.END)
        self.textbox_x2.insert(Tk.END, self.x_max)

        self.y_min = y_min
        self.textbox_y1.delete(1.0, Tk.END)
        self.textbox_y1.insert(Tk.END, self.y_min)

        self.y_max = y_max
        self.textbox_y2.delete(1.0, Tk.END)
        self.textbox_y2.insert(Tk.END, self.y_max)
