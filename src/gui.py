#!/usr/bin/env python
# gui.py - GUI management

import sys
import Tkinter as Tk
import matplotlib
import logging
import settings

from defines import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure as Mat_figure

matplotlib.use('TkAgg')

# Create root widget
root = Tk.Tk()

numberCams = None
cameraInst = None

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

    def __start(self):
        # Disable buttons that change settings
        self.check_button_1.config(state=Tk.DISABLED)
        self.check_button_2.config(state=Tk.DISABLED)
        self.check_button_3.config(state=Tk.DISABLED)
        self.check_button_4.config(state=Tk.DISABLED)

        # Get ROI size

        # todo: Initialize camera etc

    def __quit(self):
        # End program
        logging.info("Ending program")
        root.quit()
        root.destroy()
        sys.exit()

    def __init__(self, ROI):

        # Initialize buttons
        self.check_button_1 = self.check_button_2 = self.check_button_3 = self.check_button_4 = None

        # Get current settings
        self.curr_settings = settings.get_parameters()

        # Create GUI
        self.__create_gui()

    def __create_gui(self):

        # Create GUI elements and add them to root widget
        self.check_button_1 = Tk.Checkbutton(master=root, text="Show curves", command=lambda: settings.flip_parameter(settings.IDX_CAMERA))
        self.check_button_1.pack(side=Tk.LEFT)
        if self.curr_settings[IDX_CAMERA]:
            self.check_button_1.toggle()

        self.check_button_2 = Tk.Checkbutton(master=root, text="Motion detection", command=lambda: settings.flip_parameter(settings.IDX_MOTION))
        self.check_button_2.pack(side=Tk.LEFT)
        if self.curr_settings[IDX_MOTION]:
            self.check_button_2.toggle()

        self.check_button_3 = Tk.Checkbutton(master=root, text="Store frames", command=lambda: settings.flip_parameter(settings.IDX_FRAMES))
        self.check_button_3.pack(side=Tk.LEFT)
        if self.curr_settings[IDX_FRAMES]:
            self.check_button_3.toggle()

        self.check_button_4 = Tk.Checkbutton(master=root, text="Send trigger", command=lambda: settings.flip_parameter(settings.IDX_TRIGGER))
        self.check_button_4.pack(side=Tk.LEFT)
        if self.curr_settings[IDX_TRIGGER]:
            self.check_button_4.toggle()

        button_quit = Tk.Button(master=root, text='Quit', command=self.__quit)
        button_quit.pack(side=Tk.RIGHT)
        button_start = Tk.Button(master=root, text='Start video', command=self.__start)
        button_start.pack(side=Tk.RIGHT)


class ToolbarROI(Tk.Frame):
    # This toolbar allows to adjust the region-of-interest (ROI)


    def __init__(self, parent):

        # Initialize variables
        self.x_min = self.x_max = self.y_min = self.y_max = 0
        global numberCams
        self.num = numberCams

        # Create GUI
        self.__create_gui(self)


    def __create_gui(self, parent):
        # Create GUI elements and add them to root widget

        text_frame = Tk.Frame(root, width=500, height=100)
        text_frame.pack()

        # Fill list with available cameras and add to menu
        listCameras = ['']
        for cam_idx in range(self.num):
            tmp_string = "Camera " + str(cam_idx)
            listCameras.append(tmp_string)
        listCameras.pop(0)
        listCamerasStr = Tk.StringVar()
        dropDownList = Tk.OptionMenu(text_frame, listCamerasStr, *listCameras)
        listCamerasStr.set(listCameras[0])
        dropDownList.pack(side=Tk.LEFT)

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
    def __init__(self, parent):

        # Call super class
        Tk.Frame.__init__(self, parent)

        logging.info('Creating part of the GUI that shows video')
        self.video_display = WindowVideo(self)

        logging.info('Creating part of the GUI that shows the signal extracted from the video')
        self.signal_display = WindowSignal(self)

        logging.info('Creating status bar')
        self.statusbar = Statusbar(self)

        logging.info('Creating toolbar for ROI definition')
        self.toolbar_roi = ToolbarROI(self)

        logging.info('Creating toolbar with buttons')
        self.toolbar_buttons = ToolbarButtons(self)


def update(gui):
    # todo: Update frames, values, etc.

    # Restart
    root.after(10, update, gui)


def init(cameraInstance):

    # Get number of cameras
    global numberCams, cameraInst
    numberCams = cameraInstance.getNumberOfCameras()

    # Create GUI
    logging.info('GUI creation has started')
    gui = MainGUI(root)

    # Start schedular that gets current values
    root.after(1000, update, gui)

    # Start Tkinter event loop
    root.mainloop()
