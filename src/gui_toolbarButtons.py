#!/usr/bin/env python
# gui.py - GUI element: toolbar with Buttons

import sys
import Tkinter as Tk
import logging
import settings
import threading

from defines import *


# Initialize global variables
root = cameraInstance = None


class ToolbarButtons(Tk.Frame):
    # This toolbar allows the user to change settings

    def __start(self):
        logging.info("Start button has been pressed")

        # Get Event
        self.eventCameraChosen = self.cameraInstance.getEventCameraChosen()

        # Disable buttons that change settings
        self.check_button_1.config(state=Tk.DISABLED)
        self.check_button_2.config(state=Tk.DISABLED)
        self.check_button_3.config(state=Tk.DISABLED)
        self.check_button_4.config(state=Tk.DISABLED)
        self.button_start.config(state=Tk.DISABLED)
        self.dropDownList.config(state=Tk.DISABLED)

        # Give camera thread index of camera
        logging.info("Camera is started")
        chosenCamera = self.listCamerasStr.get()[-1]
        self.cameraInstance.setCameraIdx(chosenCamera)

        # Update event for camera event
        logging.info("Enabling event: eventCameraChosen ")
        self.eventCameraChosen.set()

    def __quit(self):
        # End program
        logging.info("User pressed ''quit'' button - now halting threads")

        # Close thread running for signal display
        self.signalDisplayInstance.closeSignalPlotterThread()
        logging.info("Signal display thread was closed")

        # If camera connection is active, close it
        self.cameraInstance.closeCameraThread()
        logging.info("Camera capture thread was closed")

        # Close GUI
        self.root.quit()
        logging.info("Tk mainloop() was halted")

        # Debug: Store all still running threads
        logging.debug(threading.enumerate())

        # Exit program
        logging.info("Program will halt now...")
        sys.exit()

    def __init__(self, parent, tk_root, thread, cam, signalDisplay):

        # Store variables
        global root
        self.root = tk_root

        # Store camera object
        self.cameraInstance = cam

        # Get number of available cameras
        self.num = self.cameraInstance.getNumberOfCameras()

        # Store thread object
        self.threadInstance = thread

        # Store connection to signal display
        self.signalDisplayInstance = signalDisplay

        # Initialize buttons
        self.check_button_1 = self.check_button_2 = self.check_button_3 = self.check_button_4 = \
        self.listCamerasStr = self.dropDownList = None

        # Get current settings
        self.curr_settings = settings.get_parameters()

        # Create GUI
        self.__create_gui()

    def __create_gui(self):

        # Fill list with available cameras and add to menu
        listCameras = ['']
        for cam_idx in range(self.num):
            tmp_string = "Camera " + str(cam_idx)
            listCameras.append(tmp_string)
        listCameras.pop(0)
        self.listCamerasStr = Tk.StringVar()
        self.dropDownList = Tk.OptionMenu(root, self.listCamerasStr, *listCameras)
        self.listCamerasStr.set(listCameras[0])
        self.dropDownList.pack(side=Tk.LEFT)

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

        self.button_quit = Tk.Button(master=root, text='Quit', command=self.__quit)
        self.button_quit.pack(side=Tk.RIGHT)
        self.button_start = Tk.Button(master=root, text='Start video', command=self.__start)
        self.button_start.pack(side=Tk.RIGHT)