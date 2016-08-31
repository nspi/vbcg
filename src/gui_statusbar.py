#!/usr/bin/env python
# -*- coding: ascii -*-
"""gui_statusbar.py - GUI element: statusbar"""

import Tkinter as Tk
import threading

# Initialize global variables
str_counter = fps_counter = fps_counter2 = root = None


class Statusbar(Tk.Frame):
    # This statusbar shows additional information
    # All values are updated from outside by using setters.

    def __init__(self, parent, tk_root):

        # Store variables
        global str_counter, fps_counter, root, fps_counter2
        self.root = tk_root
        self.str_counter = Tk.StringVar()
        self.fps_counter = Tk.StringVar()
        self.fps_counter2 = Tk.StringVar()
        self.currentInfo = Tk.StringVar()
        self.str_counter.set("0")
        self.fps_counter.set("0")
        self.fps_counter2.set("0")
        self.currentInfo.set("")

        # Create GUI
        self.__create_gui()

        # Start threads that update statusbar
        self.displayThread = threading.Thread(target=self.__update_values())
        self.displayThread.start()

    def __create_gui(self):
        # Create GUI elements and add them to root widget

        self.text_frame = Tk.Frame(root, width=500, height=100)
        self.text_frame.pack(side=Tk.TOP)

        self.label_counter_1 = Tk.Label(self.text_frame, text="Frames (displayed):")
        #self.label_counter_1.pack(side=Tk.LEFT)

        self.label_counter_2 = Tk.Label(self.text_frame, text=self.str_counter)
        #self.label_counter_2.pack(side=Tk.LEFT)

        self.label_counter_3 = Tk.Label(self.text_frame, text="        FPS Video (Top):")
        #self.label_counter_3.pack(side=Tk.LEFT)

        self.label_counter_4 = Tk.Label(self.text_frame, text=self.fps_counter)
        #self.label_counter_4.pack(side=Tk.LEFT)

        self.label_counter_5 = Tk.Label(self.text_frame, text="        FPS Signal Processing (Bottom):")
        #self.label_counter_5.pack(side=Tk.LEFT)

        self.label_counter_6 = Tk.Label(self.text_frame, text=self.fps_counter2)
        #self.label_counter_6.pack(side=Tk.LEFT)

        self.label_counter_7 = Tk.Label(self.text_frame, text="Status:")
        self.label_counter_7.pack(side=Tk.LEFT)

        self.label_counter_7 = Tk.Label(self.text_frame, text=self.currentInfo, font ="Verdana 9 bold")
        self.label_counter_7.pack(side=Tk.LEFT)

    def __update_values(self):

        # Store new values in labels
        self.label_counter_2.config(text=self.str_counter)
        self.label_counter_4.config(text=self.fps_counter)
        self.label_counter_6.config(text=self.fps_counter2)
        self.label_counter_7.config(text=self.currentInfo)

        # Repeat thread
        self.label_counter_2.after(1, self.__update_values)

    def updateInfoText(self, newText):
        self.currentInfo = newText

    def setFrameCounter(self, newValue):
        self.str_counter = str(newValue)

    def setFPSCounter(self, newValue):
        self.fps_counter = str(newValue)

    def setFPSCounter2(self, newValue):
        self.fps_counter2 = str(newValue)