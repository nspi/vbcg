#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_video.py - tests for src/video.py"""

import unittest
import nose
import threading
import numpy as np
import video

from nose.tools import assert_is_instance, assert_false


class Test(unittest.TestCase):

    def setUp(self):
        # Create thread
        self.videoThread = video.VideoThread()
        self.videoThread.start()

    def tearDown(self):
        # Kill thread
        self.videoThread.closeCameraThread()

    # Test if getter return correct types BEFORE start button has been pressed

    def test_getEventCameraReady(self):
        assert_is_instance(self.videoThread.getEventCameraReady(), threading._Event)

    def test_getEventCameraChosen(self):
        assert_is_instance(self.videoThread.getEventCameraChosen(), threading._Event)

    def test_getFrame(self):
        ret_1, ret_2 = self.videoThread.getFrame()
        assert_false(ret_1)
        assert_is_instance( ret_2, np.ndarray )

    def test_getNumberofCameras(self):
        assert_is_instance( self.videoThread.getNumberOfCameras(), int)

    # Test if getter return correct types AFTER start button has been pressed

    def test_getEventCameraReady_after(self):
        self.videoThread.getEventCameraChosen().set()
        yield self.test_getEventCameraReady()

    def test_getEventCameraChosen_after(self):
        self.videoThread.getEventCameraChosen().set()
        yield self.test_getEventCameraReady()

    def test_getFrame_after(self):
        self.videoThread.getEventCameraChosen().set()
        yield self.test_getEventCameraReady()

    def test_getNumberofCameras_after(self):
        self.videoThread.getEventCameraChosen().set()
        yield self.test_getEventCameraReady()

if __name__ == '__main__':
    nose.main()

