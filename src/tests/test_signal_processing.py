#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_signal_processing.py - tests for src/signal_processing.py"""

import unittest
import nose
import numpy as np

from signal_processing import SignalProcessor
from nose.tools import assert_is_instance, assert_false

class Test(unittest.TestCase):

    def setUp(self):
        # Create instance
        self.signal_processor = SignalProcessor()

    def test_normalize(self):
        assert_is_instance(self.signal_processor.normalize(np.random.rand(100)), np.ndarray)

    def test_filterWaveform(self):
        ret_1, ret_2 = self.signal_processor.filterWaveform(np.random.rand(100),
                                                            np.random.rand(100),
                                                            np.random.randint(10)+10,
                                                            np.random.randint(10)+10)
        assert_false(ret_1)
        assert_is_instance( ret_2, np.ndarray )

    def test_computeHR(self):
        ret_1, ret_2, ret_3, ret_4 = self.signal_processor.computeHR(np.random.rand(100), np.random.randint(10) + 10)
        assert_is_instance(ret_1, float)
        assert_is_instance(ret_2, np.ndarray)
        assert_is_instance(ret_3, np.ndarray)
        assert_is_instance(ret_4, int)

if __name__ == '__main__':
    nose.main()

