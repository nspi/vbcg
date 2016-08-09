#!/usr/bin/env python
# gui.py - GUI element: statusbar

import Tkinter as Tk

# Initialize global variables
str_counter = fps_counter = root = None


class Statusbar(Tk.Frame):
    # This statusbar shows additional information

    def __init__(self, parent, tk_root):

        # Store variables
        global str_counter,fps_counter,root
        self.root = tk_root
        self.str_counter = Tk.StringVar()
        self.fps_counter = Tk.StringVar()
        self.str_counter.set("0")
        self.fps_counter.set("0")

        # Create GUI
        self.__create_gui(self.str_counter, self.fps_counter)

    def __create_gui(self, parent, *args, **kwargs):
        # Create GUI elements and add them to root widget

        text_frame = Tk.Frame(root, width=500, height=100)
        text_frame.pack()

        label_counter_1 = Tk.Label(text_frame, text="Frames:")
        label_counter_1.pack(side=Tk.LEFT)

        label_counter_2 = Tk.Label(text_frame, textvariable=self.str_counter)
        label_counter_2.pack(side=Tk.LEFT)

        label_counter_3 = Tk.Label(text_frame, text="FPS:")
        label_counter_3.pack(side=Tk.LEFT)

        label_counter_4 = Tk.Label(text_frame, textvariable=self.fps_counter)
        label_counter_4.pack(side=Tk.LEFT)

    def update_values(self, new_str_value, new_fps_value):
        # Update values shown in status bar

        if isinstance(new_str_value, basestring):
            self.str_counter.set(new_str_value)

        if isinstance(new_fps_value, basestring):
            self.fps_counter.set(new_fps_value)
