#!/usr/bin/env python
# gui.py - GUI management

import sys
import Tkinter as Tk
import tkMessageBox
import matplotlib
import logging

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure as Mat_figure

matplotlib.use('TkAgg')

# Create root widget
root = Tk.Tk()


class WindowVideo(Tk.Frame):
    # In this frame the video stream is shown

    def __init__(self, parent, *args, **kwargs):

        # Create GUI
        self.__create_gui()

    def __create_gui(self):
        # Create GUI elements and add them to root widget

        video_frame = Tk.Frame(root, width=500, height=400)
        video_frame.config(background="gray")
        video_frame.pack()


class WindowSignal(Tk.Frame):
    # In this frame the signal extracted from the video stream is shown

    def __init__(self, parent, *args, **kwargs):

        # Create GUI
        self.__create_gui()

    def __create_gui(self):
        figure = Mat_figure(figsize=(5, 4), dpi=100)
        figure.add_subplot(111)

        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.show()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


class ToolbarButtons(Tk.Frame):
    # This toolbar allows the user to change settings

    def __init__(self, parent, *args, **kwargs):

        # Create GUI
        self.__create_gui()

    def __create_gui(self):
        # Create GUI elements and add them to root widget

        button = Tk.Button(master=root, text='Quit', command=quit)
        button.pack(side=Tk.RIGHT)
        button_2 = Tk.Checkbutton(master=root, text="Show curves")
        button_2.pack(side=Tk.LEFT)
        button_3 = Tk.Checkbutton(master=root, text="Motion detection")
        button_3.pack(side=Tk.LEFT)
        button_4 = Tk.Checkbutton(master=root, text="Store frames")
        button_4.pack(side=Tk.LEFT)
        button_5 = Tk.Checkbutton(master=root, text="Send trigger")
        button_5.pack(side=Tk.LEFT)


class ToolbarROI(Tk.Frame):
    # This toolbar allows to adjust the region-of-interest (ROI)

    # Initialize variables
    x_min = x_max = y_min = y_max = 0

    def __init__(self, parent, *args, **kwargs):

        # Create GUI
        self.__create_gui()

    def __create_gui(self):
        # Create GUI elements and add them to root widget

        text_frame = Tk.Frame(root, width=500, height=100)
        text_frame.pack()

        label_x1 = Tk.Label(text_frame, text="X Begin:")
        label_x1.pack(side=Tk.LEFT)
        textbox_x1 = Tk.Text(text_frame, width=10, height=1)
        textbox_x1.pack(side=Tk.LEFT)
        textbox_x1.insert(Tk.END, ToolbarROI.x_min)

        label_x2 = Tk.Label(text_frame, text="X End:")
        label_x2.pack(side=Tk.LEFT)
        textbox_x2 = Tk.Text(text_frame, width=10, height=1)
        textbox_x2.pack(side=Tk.LEFT)
        textbox_x2.insert(Tk.END, ToolbarROI.x_max)

        label_y1 = Tk.Label(text_frame, text="Y Begin:")
        label_y1.pack(side=Tk.LEFT)
        textbox_y1 = Tk.Text(text_frame, width=10, height=1)
        textbox_y1.pack(side=Tk.LEFT)
        textbox_y1.insert(Tk.END, ToolbarROI.y_min)

        label_y2 = Tk.Label(text_frame, text="Y End:")
        label_y2.pack(side=Tk.LEFT)
        textbox_y2 = Tk.Text(text_frame, width=10, height=1)
        textbox_y2.pack(side=Tk.LEFT)
        textbox_y2.insert(Tk.END, ToolbarROI.y_max)


class Statusbar(Tk.Frame):
    # This statusbar shows additional information

    # Initialize variables
    str_counter = fps_counter = None

    def __init__(self, parent, *args, **kwargs):

        # Create variables
        Statusbar.str_counter = Tk.StringVar()
        Statusbar.fps_counter = Tk.StringVar()
        Statusbar.str_counter.set("0")
        Statusbar.fps_counter.set("0")

        # Create GUI
        self.__create_gui(Statusbar.str_counter, Statusbar.fps_counter)

    def __create_gui(self, parent, *args, **kwargs):

        # Create GUI elements and add them to root widget

        text_frame = Tk.Frame(root, width=500, height=100)
        text_frame.pack()

        label_counter_1 = Tk.Label(text_frame, text="Frames:")
        label_counter_1.pack(side=Tk.LEFT)

        label_counter_2 = Tk.Label(text_frame, textvariable=Statusbar.str_counter)
        label_counter_2.pack(side=Tk.LEFT)

        label_counter_3 = Tk.Label(text_frame, text="FPS:")
        label_counter_3.pack(side=Tk.LEFT)

        label_counter_4 = Tk.Label(text_frame, textvariable=Statusbar.fps_counter)
        label_counter_4.pack(side=Tk.LEFT)

    # Update values shows in status bar
    def update_values(self, new_str_value, new_fps_value):

        if isinstance(new_str_value, basestring):
            Statusbar.str_counter.set(new_str_value)

        if isinstance(new_fps_value, basestring):
            Statusbar.fps_counter.set(new_fps_value)


class MainGUI(Tk.Frame):
    def __init__(self, parent, *args, **kwargs):

        # Call super class
        Tk.Frame.__init__(self, parent, *args, **kwargs)

        # Part of the GUI that shows video
        self.video_display = WindowVideo(self)
        # Part of the GUI that shows the signal extracted from the video
        self.signal_display = WindowSignal(self)
        # A statusbar that shows some additionall information (FPS etc)
        self.statusbar = Statusbar(self)
        # A toolbar that allows the user to adjust the ROI
        self.toolbar_roi = ToolbarROI(self)
        # A toolbar that allows the user to change settings
        self.toolbar_buttons = ToolbarButtons(self)


def update(gui):
    # todo: Update frames, values, etc.

    # Restart
    root.after(10, update, gui)


def quit():
    # End program
    root.quit()
    root.destroy()
    sys.exit()

def init():
    # Ask if the user wants to use the camera or frames from hard drive
    # question_src = tkMessageBox.askyesno("Set-up", "Do you want to use a live video from an OpenCV compatible camera "
    #                                               "(YES) or already recorded frames from your hard drive (NO)?")
    #
    #if not question_src:
    #    logging.error('Using frames from hard disk is (not yet) possible')
    #    tkMessageBox.showerror("Error", "Sorry, this is not available yet.")
    #    sys.exit()
    #else:

    logging.info('GUI creation has started')
    # Create GUI elements
    gui = MainGUI(root)
    # Start schedular that gets current values
    root.after(1000, update, gui)
    # Start Tkinter event loop
    root.mainloop()
