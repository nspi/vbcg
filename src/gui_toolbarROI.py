#!/usr/bin/env python
# gui.py - GUI element: toolbar

import Tkinter as Tk
import settings
import logging

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
        self.__create_gui(self)


    def __create_gui(self, parent):
        # Create GUI elements and add them to root widget

        self.text_frame = Tk.Frame(root, width=500, height=100)
        self.text_frame.pack()

        # Add Checkbutton to decide whether to use Viola-Jones algorithm or manual ROI definition
        curr_settings = settings.get_parameters()

        self.check_button_1 = Tk.Checkbutton(master=self.text_frame, text="Use Viola-Jones Algorithm", command=lambda: self.__viola_jones() )
        self.check_button_1.pack(side=Tk.LEFT)
        if curr_settings[IDX_FACE]:
            self.check_button_1.toggle()

        # Add Textboxes for ROI definition
        self.label_x1 = Tk.Label(self.text_frame, text="X Begin:")
        self.label_x1.pack(side=Tk.LEFT)
        self.textbox_x1 = Tk.Text(self.text_frame, width=10, height=1)
        self.textbox_x1.pack(side=Tk.LEFT)
        self.textbox_x1.insert(Tk.END, self.x_min)

        self.label_x2 = Tk.Label(self.text_frame, text="X End:")
        self.label_x2.pack(side=Tk.LEFT)
        self.textbox_x2 = Tk.Text(self.text_frame, width=10, height=1)
        self.textbox_x2.pack(side=Tk.LEFT)
        self.textbox_x2.insert(Tk.END, self.x_max)

        self.label_y1 = Tk.Label(self.text_frame, text="Y Begin:")
        self.label_y1.pack(side=Tk.LEFT)
        self.textbox_y1 = Tk.Text(self.text_frame, width=10, height=1)
        self.textbox_y1.pack(side=Tk.LEFT)
        self.textbox_y1.insert(Tk.END, self.y_min)

        self.label_y2 = Tk.Label(self.text_frame, text="Y End:")
        self.label_y2.pack(side=Tk.LEFT)
        self.textbox_y2 = Tk.Text(self.text_frame, width=10, height=1)
        self.textbox_y2.pack(side=Tk.LEFT)
        self.textbox_y2.insert(Tk.END, self.y_max)

    def __viola_jones(self):
        # Action to perform when Viola-Jones button is pressed
        settings.flip_parameter(settings.IDX_FACE)

        # Get current parameters
        curr_settings = settings.get_parameters()

        if curr_settings[IDX_FACE]:
            self.textbox_x1.config(state=Tk.DISABLED,bg='gray')
            self.textbox_x2.config(state=Tk.DISABLED,bg='gray')
            self.textbox_y1.config(state=Tk.DISABLED,bg='gray')
            self.textbox_y2.config(state=Tk.DISABLED,bg='gray')
            logging.info('Viola-Jones algorithm was activated by the user')
        else:
            self.textbox_x1.config(state=Tk.NORMAL,bg='white')
            self.textbox_x2.config(state=Tk.NORMAL,bg='white')
            self.textbox_y1.config(state=Tk.NORMAL,bg='white')
            self.textbox_y2.config(state=Tk.NORMAL,bg='white')
            logging.info('Viola-Jones algorithm was disabled by the user')

