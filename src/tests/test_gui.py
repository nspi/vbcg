#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_gui.py - tests for all GUI elements"""

# Needed so that Travis CI can find cv2.so
import sys
sys.path.insert(0, '/usr/lib/pyshared/python2.7')

# Disabling this test class because of incompatibility with Travis CI
__test__ = 0

import nose
import video
import gui
import Tkinter as tk
import settings
import time

from defines import *
from nose.tools import assert_is_instance, assert_equal, assert_true, assert_not_equal


class Test(object):

    def setUp(self):
        """ Initialize GUI and GUI elements """

        # Create video thread
        self.videoThread = video.VideoThread()
        self.videoThread.start()

        # Create and start GUI
        self.guiThread = gui.GUI()
        self.guiThread.start(self.videoThread)

        # Get window
        self.mainWindow = self.guiThread.get_window()

        # Get GUI elements
        self.toolbar_roi = self.mainWindow.get_toolbar_roi()
        self.toolbar_buttons = self.mainWindow.get_toolbar_buttons()
        self.statusbar = self.mainWindow.get_statusbar()
        self.winSignal = self.mainWindow.get_signal_display()
        self.winVideo = self.mainWindow.get_video_display()

    def tearDown(self):

        # Close threads
        self.winSignal.closeThreads()
        self.guiThread.clear()
        self.videoThread.close_camera_thread()

        # Waiting for threads to close
        time.sleep(3)

    # gui_windowVideo.py

    def test_gui_VideoDisplay_get_frame_counter(self):
        """Check if number of frames is well-defined"""
        ret_1 = self.winVideo.get_frame_counter()
        assert_is_instance(ret_1, int)

    def test_gui_VideoDisplay_set_heart_rate_text(self):
        """ Check if HR Text can be set"""
        self.winVideo.set_heart_rate_text("60")
        assert_equal(self.winVideo.HeartRateText, "60")

    def test_gui_VideoDisplay_display_heart_trigger(self):
        """ Check if event can be set"""
        self.winVideo.display_heart_trigger()
        assert_true(self.winVideo.eventShowTrigger.is_set())

    # gui_toolbarButtons.py

    def test_gui_toolbarButtons_change_algorithm(self):
        """Check if change algorithm button function works"""

        # Get current text in text box
        curr_text = self.toolbar_buttons.dropDownListAlgorithm.cget("text")
        # Call function
        self.toolbar_buttons._ToolbarButtons__change_algorithm()
        # Get options
        curr_settings = settings.get_parameters()

        if curr_settings[IDX_ALGORITHM] == 0 and curr_text == LABEL_ALGORITHM_1:
            assert True
        elif curr_settings[IDX_ALGORITHM] == 1 and curr_text == LABEL_ALGORITHM_2:
            assert True
        elif curr_settings[IDX_ALGORITHM] == 2 and curr_text == LABEL_ALGORITHM_3:
            assert True
        else:
            assert False

    def test_gui_toolbarButtons_start_button(self):
        """Check if activation of start button has an effect"""
        self.toolbar_buttons._ToolbarButtons__start()
        assert_true(self.toolbar_buttons.eventCameraChosen.is_set())

    def test_gui_toolbarButtons_quit_button(self):
        """Check if activation of quit button has an effect"""
        self.toolbar_buttons._ToolbarButtons__quit()
        assert_true(self.toolbar_buttons.cameraInstance.eventProgramEnd.is_set())

    # gui_toolbarROI.py

    def test_gui_ToolbarROI_get_roi(self):
        """Check if ROI values are well-defined """
        ret_1, ret_2, ret_3, ret_4 = self.toolbar_roi.get_roi()
        assert_is_instance(ret_1, int)
        assert_is_instance(ret_2, int)
        assert_is_instance(ret_3, int)
        assert_is_instance(ret_4, int)

    def test_gui_ToolbarROI_set_roi_in_gui(self):
        """Check if ROI values can be set using GUI"""
        self.toolbar_roi.set_roi(0, 255, 0, 255)
        assert_equal(self.toolbar_roi.x_min, 0)
        assert_equal(self.toolbar_roi.x_max, 255)
        assert_equal(self.toolbar_roi.y_min, 0)
        assert_equal(self.toolbar_roi.y_max, 255)

    def test_gui_ToolbarROI__store_roi(self):
        """Check if ROI values can be set using a wrongly-defined minimum"""
        self.toolbar_roi.set_roi(300, 255, 300, 255)
        self.toolbar_roi._ToolbarROI__store_roi()
        assert_equal(self.toolbar_roi.x_min, 0)
        assert_equal(self.toolbar_roi.x_max, 255)
        assert_equal(self.toolbar_roi.y_min, 0)
        assert_equal(self.toolbar_roi.y_max, 255)

    def test_gui_ToolbarROI_enable_disable_Viola_Jones(self):
        """Check is Viola Jones button function works"""

        # Get options before
        curr_settings = settings.get_parameters()
        before = curr_settings[IDX_FACE]
        # Simulate button click
        self.toolbar_roi._ToolbarROI__enable_or_disable_viola_jones_algorithm()
        # Get options after
        curr_settings = settings.get_parameters()
        after = curr_settings[IDX_FACE]
        # Restore value
        settings.change_parameter(IDX_FACE, before)

        # Compare
        assert_not_equal(before, after)

    def test_gui_ToolbarROI___enable_or_disable_option(self):
        """Check if zero padding button function works"""

        # Get options before
        curr_settings = settings.get_parameters()
        before = curr_settings[IDX_ZERO_PADDING]
        # Simulate button click
        self.toolbar_roi._ToolbarROI__enable_or_disable_option(IDX_ZERO_PADDING)
        # Get options after
        curr_settings = settings.get_parameters()
        after = curr_settings[IDX_ZERO_PADDING]
        # Restore value
        settings.change_parameter(IDX_ZERO_PADDING, before)

        # Compare
        assert_not_equal(before, after)

    # Test simple getter

    def test_gui_getStatusbar(self):
        assert_is_instance(self.statusbar, gui.Statusbar)

    def test_gui_getToolbarButtons(self):
        assert_is_instance(self.toolbar_buttons, gui.ToolbarButtons)

    def test_gui_ToolbarROI(self):
        assert_is_instance(self.toolbar_roi, gui.ToolbarROI)

    def test_gui_VideoDisplay(self):
        assert_is_instance(self.winVideo, gui.WindowVideo)

    def test_gui_SignalDisplay(self):
        assert_is_instance(self.winSignal, gui.WindowSignal)

    def test_gui_Root(self):
        assert_is_instance(self.mainWindow.get_root(), tk.Tk)

if __name__ == '__main__':
    nose.main()
