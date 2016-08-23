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
        self.button_start.config(state=Tk.DISABLED)
        self.dropDownListCamera.config(state=Tk.DISABLED)
        self.dropDownListAlgorithm.config(state=Tk.DISABLED)
        self.textbox_fps.config(state=Tk.DISABLED)
        self.textbox_fps.config(bg='lightgray')

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
        self.listCamerasStr = self.dropDownListCamera = self.listAlgorithmStr = self.dropDownListAlgorithm =  None

        # Get current settings
        self.curr_settings = settings.get_parameters()

        # Create GUI
        self.__create_gui()

    def __create_gui(self):

        self.button_frame = Tk.Frame(root, width=500, height=100)
        self.button_frame.pack(side=Tk.BOTTOM)

        # Fill list with available cameras and add to menu
        self.label_x0 = Tk.Label(self.button_frame, text="Camera:")
        self.label_x0.pack(side=Tk.LEFT)
        listCameras = ['']
        for cam_idx in range(self.num):
            tmp_string = str(cam_idx)
            listCameras.append(tmp_string)
        listCameras.pop(0)
        self.listCamerasStr = Tk.StringVar()
        self.dropDownListCamera = Tk.OptionMenu(self.button_frame, self.listCamerasStr, *listCameras)
        self.listCamerasStr.set(listCameras[0])
        self.dropDownListCamera.pack(side=Tk.LEFT)
        # Todo: Load default camera from settings

        self.label_x1 = Tk.Label(self.button_frame, text="FPS:")
        self.label_x1.pack(side=Tk.LEFT)
        self.textbox_fps = Tk.Text(self.button_frame, width=5, height=1)
        self.textbox_fps.pack(side=Tk.LEFT)
        self.textbox_fps.insert(Tk.END, "30")

        # Fill list with available algorithms and add to menu
        self.label_x2 = Tk.Label(self.button_frame, text="Algorithm:")
        self.label_x2.pack(side=Tk.LEFT)
        listAlgorithms = ['']
        listAlgorithms.append("HR estimation")
        #listAlgorithms.append("Algorithm #2")
        #listAlgorithms.append("Algorithm #3")
        listAlgorithms.pop(0)
        self.listAlgorithmStr = Tk.StringVar()
        self.dropDownListAlgorithm = Tk.OptionMenu(self.button_frame, self.listAlgorithmStr, *listAlgorithms,
                                                   command=lambda _: self.__changeAlgorithm())
        self.listAlgorithmStr.set(listAlgorithms[0])
        self.dropDownListAlgorithm.pack(side=Tk.LEFT)
        # Todo: Load default algorithm from settings

        # Create GUI elements for options and add them to menu
        self.check_button_1 = Tk.Checkbutton(master=self.button_frame, text="Show curves",
                                             command=lambda: settings.flip_parameter(settings.IDX_CURVES))
        self.check_button_1.pack(side=Tk.LEFT)
        if self.curr_settings[IDX_CURVES]:
            self.check_button_1.toggle()

        self.check_button_2 = Tk.Checkbutton(master=self.button_frame, text="Motion detection",
                                             command=lambda: settings.flip_parameter(settings.IDX_MOTION))
        self.check_button_2.pack(side=Tk.LEFT)
        if self.curr_settings[IDX_MOTION]:
            self.check_button_2.toggle()
        self.check_button_2.config(state=Tk.DISABLED)

        self.check_button_3 = Tk.Checkbutton(master=self.button_frame, text="Store frames",
                                             command=lambda: settings.flip_parameter(settings.IDX_FRAMES))
        self.check_button_3.pack(side=Tk.LEFT)
        if self.curr_settings[IDX_FRAMES]:
            self.check_button_3.toggle()

        self.button_quit = Tk.Button(master=self.button_frame, text='Quit', command=self.__quit)
        self.button_quit.pack(side=Tk.RIGHT)
        self.button_start = Tk.Button(master=self.button_frame, text='Start', command=self.__start)
        self.button_start.pack(side=Tk.RIGHT)

    def __changeAlgorithm(self):
        if self.dropDownListAlgorithm.cget("text") == "HR estimation":
            settings.change_parameter(IDX_ALGORITHM,1)
        #elif self.dropDownListAlgorithm.cget("text") == "Algorithm #2":
        #    settings.change_parameter(IDX_ALGORITHM, 2)
        #else:
        #    settings.change_parameter(IDX_ALGORITHM, 3)
