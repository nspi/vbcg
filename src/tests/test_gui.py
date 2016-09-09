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
import settings
import time
import datetime

from defines import *
from nose.tools import assert_is_instance, assert_equal, assert_true, assert_not_equal, assert_dict_contains_subset


class Test(unittest.TestCase):

    def setUp(self):
        """ Initialize GUI and GUI elements """
        print "Start setUp"
        print datetime.datetime.now()

        # Create video thread
        print "Starting video thread"
        print datetime.datetime.now()
        self.videoThread = video.VideoThread()
        self.videoThread.start()

        # Reload gui module (because of global Tk.Tk())
        print "Reload gui.py"
        print datetime.datetime.now()
        reload(gui)

        # Create GUI
        print "Create gui thread"
        print datetime.datetime.now()
        self.guiThread = gui.GUI()
        self.guiThread.start(self.videoThread)

        # Get window
        print "Get main window"
        print datetime.datetime.now()
        self.mainWindow = self.guiThread.get_window()

        # Get GUI elements
        print "Get gui elements"
        print datetime.datetime.now()
        self.toolbar_roi = self.mainWindow.get_toolbar_roi()
        self.toolbar_buttons = self.mainWindow.get_toolbar_buttons()
        self.statusbar = self.mainWindow.get_statusbar()
        self.winSignal = self.mainWindow.get_signal_display()
        self.winVideo = self.mainWindow.get_video_display()

        print "Starting test"
        print datetime.datetime.now()

    def tearDown(self):
        """Destroy GUI"""

        print "Test has ended, starting teardown"
        print datetime.datetime.now()

        # Close threads
        self.winSignal.closeThreads()
        self.guiThread.clear()
        self.videoThread.close_camera_thread()

        print "teardown has ended. "
        print datetime.datetime.now()

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

        if curr_settings[IDX_ALGORITHM] == 0 and curr_text == "Estimate Heart rate":
            assert True
        elif curr_settings[IDX_ALGORITHM] == 1 and curr_text == "Filter waveform":
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

    def test_gui_ToolbarROI_enable_or_disable_fft_zero_padding(self):
        """Check if zero padding button function works"""

        # Get options before
        curr_settings = settings.get_parameters()
        before = curr_settings[IDX_ZERO_PADDING]
        # Simulate button click
        self.toolbar_roi._ToolbarROI__enable_or_disable_fft_zero_padding()
        # Get options after
        curr_settings = settings.get_parameters()
        after = curr_settings[IDX_ZERO_PADDING]
        # Restore value
        settings.change_parameter(IDX_ZERO_PADDING, before)

        # Compare
        assert_not_equal(before, after)

    def test_gui_signalProcessor(self):
        """Check if output of gui_signalProcessor.py contains correct dictionary"""

        # Store old FPS
        self.curr_settings = settings.get_parameters()
        self.fps_backup = self.curr_settings[IDX_FPS]

        # Adjust to FPS of test video
        settings.change_parameter(IDX_FPS, 25)

        # Store frame location in video thread
        file_names = ["1.jpg"]
        for num in range(2, 1000):
            file_names.append(str(num) + ".jpg")
        self.videoThread.store_frames_from_disk("tests/test_frames", file_names)

        # Activate video thread
        self.videoThread.eventVideoReady.set()
        self.videoThread.eventUserPressedStart.set()

        # Get signal processor
        signal_processor = self.winSignal.get_signal_processor()

        # Wait
        time.sleep(1)

        # Get dict
        current_dictionary = signal_processor.dict

        # Get current options
        self.currSettings = settings.get_parameters()

        # Compare returned value to expected value
        if self.currSettings[IDX_ALGORITHM] == 0:
            expected_dictionary = {'valuesOutput': 1, 'valuesOutput2': 1, 'spectrumAxis': 1, 'spectrumMax': 1}
            self.assertEquals(expected_dictionary.keys(), current_dictionary.keys())
        elif self.currSettings[IDX_ALGORITHM] == 1:
            expected_dictionary = {'valuesOutput': 1, 'valuesOutput2': 1}
            self.assertEquals(expected_dictionary.keys(), current_dictionary.keys())
        else:
            assert False

        # Restore old FPS
        settings.change_parameter(IDX_FPS, self.fps_backup)

    def test_gui_signalPlotter(self):
        """Check if gui_signalPlotter.py gets dict values from gui_signalProcessor"""

        # Store old FPS
        self.curr_settings = settings.get_parameters()
        self.fps_backup = self.curr_settings[IDX_FPS]

        # Adjust to FPS of test video
        settings.change_parameter(IDX_FPS, 25)

        # Store frame location in video thread
        file_names = ["1.jpg"]
        for num in range(2, 1000):
            file_names.append(str(num) + ".jpg")
        self.videoThread.store_frames_from_disk("tests/test_frames", file_names)

        # Activate video thread
        self.videoThread.eventVideoReady.set()
        self.videoThread.eventUserPressedStart.set()

        # Get signal plotter
        signal_plotter = self.winSignal.get_signal_plotter()

        # Wait
        time.sleep(10)

        # Check if dict contains values
        if signal_plotter.valuesOutput is not None:
            assert True
        else:
            assert False

        # Restore old FPS
        settings.change_parameter(IDX_FPS, self.fps_backup)

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
