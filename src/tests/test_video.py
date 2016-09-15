#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_video.py - tests for src/video.py"""

# Needed so that Travis CI can find cv2.so
import sys
sys.path.insert(0, '/usr/lib/pyshared/python2.7')

import nose
import threading
import numpy as np
import video
import settings
import time

from defines import *
from nose.tools import assert_is_instance, assert_false, assert_equal, assert_true


class Test(object):

    def setUp(self):
        # Create thread
        self.videoThread = video.VideoThread()
        self.videoThread.start()

    def tearDown(self):
        # Kill thread
        self.videoThread.close_camera_thread()

    # Test more complex functions

    def test_set_camera_idx(self):
        self.videoThread.set_camera_idx(5)
        assert_equal(self.videoThread.cameraIdx, 5)

    def test_store_frames_from_disk(self):
        self.videoThread.store_frames_from_disk("test_frames/", "files")
        assert_equal(self.videoThread.files, "files")
        assert_equal(self.videoThread.filesDir, "test_frames/")

    def test_close_camera_thread(self):
        assert_false(self.videoThread.eventProgramEnd.is_set())
        self.videoThread.close_camera_thread()
        assert_true(self.videoThread.eventProgramEnd.is_set())

    def test_read_frames_from_disk(self):
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
        self.videoThread.eventUserPressedStart.set()

        # Sleep
        time.sleep(4)

        # Restore old FPS
        settings.change_parameter(IDX_FPS, self.fps_backup)

    # Test simple getter

    def test_get_event_camera_ready(self):
        assert_is_instance(self.videoThread.get_event_camera_ready(), threading._Event)

    def test_get_event_camera_chosen(self):
        assert_is_instance(self.videoThread.get_event_camera_chosen(), threading._Event)

    def test_get_frame(self):
        ret_1, ret_2 = self.videoThread.get_frame()
        assert_false(ret_1)
        assert_is_instance(ret_2, np.ndarray)

    def test_get_number_of_cameras(self):
        assert_is_instance(self.videoThread.get_number_of_cameras(), int)


if __name__ == '__main__':
    nose.main()
