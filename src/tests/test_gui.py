#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_gui.py - tests for all GUI elements"""

# Needed so that Travis CI can find cv2.so
import sys
sys.path.insert(0, '/usr/lib/pyshared/python2.7')

import unittest
import nose
import video
import gui
import Tkinter as tk

from nose.tools import assert_is_instance


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """ Initialize GUI and GUI elements """

        # Create video thread
        self.videoThread = video.VideoThread()
        self.videoThread.start()

        # Create GUI
        self.guiThread = gui.GUI()
        self.mainWindow = gui.MainWindow(self.guiThread, self.videoThread)

        # Get TK root widget
        self.root = self.mainWindow.get_root()

        # Obtain GUI elements
        self.toolbar_roi = self.mainWindow.get_toolbar_roi()
        self.toolbar_buttons = self.mainWindow.get_toolbar_buttons()
        self.statusbar = self.mainWindow.get_statusbar()
        self.winSignal = self.mainWindow.get_signal_display()
        self.winVideo = self.mainWindow.get_video_display()

    @classmethod
    def tearDownClass(self):
        """Destroy GUI"""

        # Close threads
        self.videoThread.close_camera_thread()
        self.winSignal.closeThreads()

        # Close root widget
        self.root.quit()
        self.root.destroy()

    # Test more complex functions

    def test_gui_VideoDisplay_get_frameCounter(self):
        """Check if number of frames is well-defined"""
        ret_1 = self.winVideo.get_frame_counter()
        assert_is_instance(ret_1, int)

    def test_gui_ToolbarROI_getROI(self):
        """Check if ROI values are well-defined """
        ret_1, ret_2, ret_3, ret_4 = self.toolbar_roi.get_roi()
        assert_is_instance(ret_1, int)
        assert_is_instance(ret_2, int)
        assert_is_instance(ret_3, int)
        assert_is_instance(ret_4, int)

    # Test simple getter

    def test_gui_getStatusbar(self):
        assert_is_instance(self.mainWindow.get_statusbar(), gui.Statusbar)

    def test_gui_getToolbarButtons(self):
        assert_is_instance(self.mainWindow.get_toolbar_buttons(), gui.ToolbarButtons)

    def test_gui_ToolbarROI(self):
        assert_is_instance(self.mainWindow.get_toolbar_roi(), gui.ToolbarROI)

    def test_gui_VideoDisplay(self):
        assert_is_instance(self.mainWindow.get_video_display(), gui.WindowVideo)

    def test_gui_SignalDisplay(self):
        assert_is_instance(self.mainWindow.get_signal_display(), gui.WindowSignal)

    def test_gui_Root(self):
        assert_is_instance(self.mainWindow.get_root(), tk.Tk)


if __name__ == '__main__':
    nose.main()
