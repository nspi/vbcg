#!/usr/bin/env python
# gui.py - GUI element: toolbar

import Tkinter as Tk

# Initialize global variables
root = None


class ToolbarROI(Tk.Frame):
    # This toolbar allows to adjust the region-of-interest (ROI)

    def __init__(self, parent, tk_root):

        # Store variables
        global root
        self.root = tk_root
        self.x_min = self.x_max = self.y_min = self.y_max = 0

        # Create GUI
        self.__create_gui(self)


    def __create_gui(self, parent):
        # Create GUI elements and add them to root widget

        text_frame = Tk.Frame(root, width=500, height=100)
        text_frame.pack()

        # Add Textboxes for ROI definition
        label_x1 = Tk.Label(text_frame, text="X Begin:")
        label_x1.pack(side=Tk.LEFT)
        textbox_x1 = Tk.Text(text_frame, width=10, height=1)
        textbox_x1.pack(side=Tk.LEFT)
        textbox_x1.insert(Tk.END, self.x_min)

        label_x2 = Tk.Label(text_frame, text="X End:")
        label_x2.pack(side=Tk.LEFT)
        textbox_x2 = Tk.Text(text_frame, width=10, height=1)
        textbox_x2.pack(side=Tk.LEFT)
        textbox_x2.insert(Tk.END, self.x_max)

        label_y1 = Tk.Label(text_frame, text="Y Begin:")
        label_y1.pack(side=Tk.LEFT)
        textbox_y1 = Tk.Text(text_frame, width=10, height=1)
        textbox_y1.pack(side=Tk.LEFT)
        textbox_y1.insert(Tk.END, self.y_min)

        label_y2 = Tk.Label(text_frame, text="Y End:")
        label_y2.pack(side=Tk.LEFT)
        textbox_y2 = Tk.Text(text_frame, width=10, height=1)
        textbox_y2.pack(side=Tk.LEFT)
        textbox_y2.insert(Tk.END, self.y_max)