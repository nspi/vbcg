#!/usr/bin/env python
# gui.py - GUI element: toolbar

import Tkinter as Tk
import settings
import logging
import threading
import numbers

from defines import *

# Initialize global variables
root = None


class ToolbarROI(Tk.Frame):
    # This toolbar allows to adjust the region-of-interest (ROI)

    def __init__(self, parent, tk_root):

        # Store variables
        global root
        self.root = tk_root
        self.x_min = self.x_max = self.y_min = self.y_max = 0

        # Initialize buttons
        self.textbox_x1 = self.textbox_x2 = self.textbox_y1 = self.textbox_y2 = None

        # Create GUI
        self.__createGUI(self)

        # Start thread that stores ROI
        self.displayThread = threading.Thread(target=self.__storeROI)
        self.displayThread.start()


    def __createGUI(self, parent):
        # Create GUI elements and add them to root widget

        self.button_frame = Tk.Frame(root, width=500, height=100)
        self.button_frame.pack(side=Tk.BOTTOM)

        # Add Checkbutton to decide whether to use Viola-Jones algorithm or manual ROI definition
        curr_settings = settings.get_parameters()
        self.check_button_1 = Tk.Checkbutton(master=self.button_frame, text="Viola-Jones Face Detection", command=lambda: self.__violaJones())
        self.check_button_1.pack(side=Tk.LEFT)

        # Add empty box
        # Todo: add a more elegant solution
        self.label_x1 = Tk.Label(self.button_frame, text="                  ")
        self.label_x1.pack(side=Tk.LEFT)

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
        # Action to perform when Viola-Jones button is pressed
        settings.flip_parameter(settings.IDX_FACE)

        # Get current parameters
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

    def __storeROI(self):
        # Store ROI values from textboxes when it has more than 1 symbol and it contains of numbers only

        # Get values from textboxes
        if len(self.textbox_x1.get("1.0", Tk.END + "-1c"))>0 &\
              (self.textbox_x1.get("1.0", Tk.END + "-1c").isdigit() == len(self.textbox_x1.get("1.0", Tk.END + "-1c"))):
               self.x_min = int(self.textbox_x1.get("1.0", Tk.END + "-1c"))
               logging.info("ROI x_min value was set by user.")
        if len(self.textbox_x2.get("1.0", Tk.END + "-1c"))>0 &\
              (self.textbox_x2.get("1.0", Tk.END + "-1c").isdigit() == len(self.textbox_x2.get("1.0", Tk.END + "-1c"))):
               self.x_max = int(self.textbox_x2.get("1.0", Tk.END + "-1c"))
               logging.info("ROI x_max value was set by user.")

        if len(self.textbox_y1.get("1.0", Tk.END + "-1c"))>0 &\
              (self.textbox_y1.get("1.0", Tk.END + "-1c").isdigit() == len(self.textbox_y1.get("1.0", Tk.END + "-1c"))):
               self.y_min = int(self.textbox_y1.get("1.0", Tk.END + "-1c"))
               logging.info("ROI y_min value was set by user.")

        if len(self.textbox_y2.get("1.0", Tk.END + "-1c"))>0 &\
              (self.textbox_y2.get("1.0", Tk.END + "-1c").isdigit() == len(self.textbox_y2.get("1.0", Tk.END + "-1c"))):
               self.y_max = int(self.textbox_y2.get("1.0", Tk.END + "-1c"))
               logging.info("ROI y_max value was set by user.")

        # If *_min < *_max: Correct values
        if self.x_min >= self.x_max:
            self.x_min = 0
            self.textbox_x1.delete(1.0, Tk.END)
            self.textbox_x1.insert(Tk.END, 0)
            logging.warn("Your ROI definition was inadequate (x_min < x_max). The values were corrected.")
        if self.y_min >= self.y_max:
            self.y_min = 0
            self.textbox_y1.delete(1.0, Tk.END)
            self.textbox_y1.insert(Tk.END,0)
            logging.warn("Your ROI definition was inadequate (y_min < y_max). The values were corrected.")

        # Repeat thread
        self.button_frame.after(1000, lambda: self.__storeROI())

    def getROI(self):
        return self.x_min,self.x_max,self.y_min,self.y_max

    def setROI(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.textbox_x1.delete(1.0, Tk.END)
        self.textbox_x1.insert(Tk.END, self.x_min)

        self.x_max = x_max
        self.textbox_x2.delete(1.0, Tk.END)
        self.textbox_x2.insert(Tk.END,self.x_max)

        self.y_min = y_min
        self.textbox_y1.delete(1.0, Tk.END)
        self.textbox_y1.insert(Tk.END,self.y_min)

        self.y_max = y_max
        self.textbox_y2.delete(1.0, Tk.END)
        self.textbox_y2.insert(Tk.END,self.y_max)