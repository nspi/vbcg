#!/usr/bin/env python
# gui.py - GUI element: frame that displays video

import Tkinter as Tk
import threading
import Image
import ImageTk

# Initialize global variables
root = None

class WindowVideo(Tk.Frame):
    # In this frame the video stream is shown

    def __init__(self, parent, tk_root, thread, cam):

        # Store variables
        global root
        self.root = tk_root

        # Save camera object
        self.cameraInstance = cam

        # Save thread object
        self.threadInstance = thread

        # Create GUI
        self.__create_gui()

        # Start frame display as thread
        self.displayThread = threading.Thread(target=self.__show_image)
        self.displayThread.start()

    def __create_gui(self):
        # Create GUI elements and add them to root widget

        self.video_frame = Tk.Frame(root, width=500, height=400)
        self.video_frame.config(background="gray")
        self.video_frame.pack()
        self.lmain = Tk.Label(self.video_frame)
        self.lmain.pack()

    def __show_image(self):
        # Get frame from camera and display it

        self.frame = self.cameraInstance.getFrame()
        self.frameConverted = Image.fromarray(self.frame)
        self.imgTK = ImageTk.PhotoImage(image=self.frameConverted)
        self.lmain.imgtk = self.imgTK
        self.lmain.configure(image=self.imgTK)
        self.lmain.after(1, self.__show_image)