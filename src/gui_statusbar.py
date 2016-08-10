#!/usr/bin/env python
# gui.py - GUI element: statusbar

import Tkinter as Tk
import threading

# Initialize global variables
str_counter = fps_counter = root = videoInstance = None


class Statusbar(Tk.Frame):
    # This statusbar shows additional information

    def __init__(self, parent, tk_root, windowVideo):

        # Store variables
        global str_counter,fps_counter,root,videoInstance
        self.root = tk_root
        self.videoInstance = windowVideo
        self.str_counter = Tk.StringVar()
        self.fps_counter = Tk.StringVar()
        self.str_counter.set("0")
        self.fps_counter.set("0")

        # Create GUI
        self.__create_gui(self.str_counter, self.fps_counter)

        # Start threads that update statusbar
        self.displayThread = threading.Thread(target=self.__update_values())
        self.displayThread.start()

    def __create_gui(self, parent, *args, **kwargs):
        # Create GUI elements and add them to root widget

        self.text_frame = Tk.Frame(root, width=500, height=100)
        self.text_frame.pack()

        self.label_counter_1 = Tk.Label(self.text_frame, text="Frames:")
        self.label_counter_1.pack(side=Tk.LEFT)

        self.label_counter_2 = Tk.Label(self.text_frame, text=self.str_counter)
        self.label_counter_2.pack(side=Tk.LEFT)

        self.label_counter_3 = Tk.Label(self.text_frame, text="FPS (approx.):")
        self.label_counter_3.pack(side=Tk.LEFT)

        self.label_counter_4 = Tk.Label(self.text_frame, text=self.fps_counter)
        self.label_counter_4.pack(side=Tk.LEFT)

    def __update_values(self):

        # Get values
        self.str_counter = self.videoInstance.get_frameCounter()
        self.fps_counter = self.videoInstance.get_FPS()

        # Update labels
        self.label_counter_2.config(text=self.str_counter)
        self.label_counter_4.config(text=self.fps_counter)

        # Repeat thread
        self.label_counter_2.after(1, self.__update_values)
