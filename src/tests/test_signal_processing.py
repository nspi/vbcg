#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_signal_processing.py - tests for src/signal_processing.py"""

import nose
import numpy as np
import settings
import time

from defines import *
from signal_processing import SignalProcessor
from nose.tools import assert_is_instance, assert_false, assert_equal, assert_almost_equal, assert_true


class Test(object):

    def setUp(self):
        """Create instance"""
        self.signal_processor = SignalProcessor()

    def tearDown(self):
        """Clear instance"""
        self.signal_processor.clear()

    def test__curve_fit(self):
        """Test if curve fit computes approximately correct values"""

        for n in range(0, 25):

            size_signal = np.random.randint(100) + 10

            x = np.arange(0, size_signal)
            b = np.random.randint(10) + 1
            m = np.random.rand()

            yield self.curve_fit, m, x, b

    def curve_fit(self, m, x, b):
        """called by generators in test__curve_fit"""
        res = self.signal_processor._SignalProcessor__curve_fit(x, m * x + b)
        assert_almost_equal(res[0], m)

    def test_normalize(self):
        """Test if normalization returns correct object class"""
        assert_is_instance(self.signal_processor.normalize(np.random.rand(100)), np.ndarray)

    def test_nextpow2(self):
        """Check if nextpow2 returns correct value"""
        assert_equal(self.signal_processor.nextpow2(100), 128)

    def test_nextpow2_2(self):
        """Check if nextpow2 returns correct value"""
        assert_equal(self.signal_processor.nextpow2(250), 256)

    def test_nextpow2_3(self):
        """Check if nextpow2 returns correct value"""
        assert_equal(self.signal_processor.nextpow2(300), 512)

    def test_compute_zero_padding_values(self):
        """Check if zero padding returns correct value"""
        ret_1, ret_2 = self.signal_processor.compute_zero_padding_values(128)
        assert_equal(ret_1, 64)

    def test_compute_zero_padding_values_2(self):
        """Check if zero padding returns correct values"""
        ret_1, ret_2 = self.signal_processor.compute_zero_padding_values(128)
        assert_equal(ret_1, ret_2)

    def test_filter_waveform_return_false(self):
        """Running the algorithm with this parameter combination should not never result in a trigger"""

        for n in range(0, 25):
            signal_1 = np.random.rand(100)
            signal_2 = np.random.rand(100)
            param_1 = np.random.randint(10) + 1
            param_2 = np.random.randint(10) + 1
            param_3 = np.inf
            yield self.filter_waveform_trigger_false, signal_1, signal_2, param_1, param_2, param_3

        for n in range(0, 25):
            signal_1 = np.random.rand(100)
            signal_2 = np.random.rand(100)
            param_1 = np.random.randint(10) + 1
            param_2 = 1
            param_3 = 0
            yield self.filter_waveform_trigger_false, signal_1, signal_2, param_1, param_2, param_3

    def filter_waveform_trigger_false(self, signal_1, signal_2, param_1, param_2, param_3):
        """Called by test generators in test_filter_waveform_return_false"""
        ret_1, _ = self.signal_processor.filter_waveform(signal_1, signal_2, param_1, param_2, param_3)
        assert_false(ret_1)

    def test_filter_waveform_trigger_true(self):
        """Running the algorithm with this parameters should result in a trigger"""
        for n in range(0, 25):
            test_signal = np.random.rand(100)
            param_1 = 10
            param_2 = 2
            param_3 = 0.1
            yield self.filter_waveform_trigger_true, test_signal, np.zeros(100), param_1, param_2, param_3

    def filter_waveform_trigger_true(self, signal_1, signal_2, param_1, param_2, param_3):
        """Called by test generators in test_filter_waveform_trigger_true"""

        # Sleep a bit longer, just to be safe that we waited longer than param_3
        time.sleep(param_3 + 0.1)

        ret_1, ret_2 = self.signal_processor.filter_waveform(signal_1, signal_2, param_1, param_2, param_3)
        ret_1, ret_2 = self.signal_processor.filter_waveform(signal_1, ret_2, param_1, param_2, param_3)
        ret_1, ret_2 = self.signal_processor.filter_waveform(signal_1, ret_2, param_1, param_2, param_3)

        assert_true(ret_1)

    def test_filter_waveform_return_true(self):

        # Create random input signal
        input_signal = np.random.rand(100)

        # Initialize second signal
        input_signal_2 = np.ones(1)

        # This configuration of filter_waveform() should return true
        # (if time passed is > 0.5 and input_signal_2 is stable for 3 values)
        for num in range(0, 4):
            ret_1, ret_2 = self.signal_processor.filter_waveform(input_signal, input_signal_2, 9, 3, 0.5)
            input_signal_2 = ret_2
            time.sleep(0.5)

        assert_true(ret_1)
        assert_is_instance(ret_2, np.ndarray)

    def test_compute_heart_rate_frequency(self):
        """Test if HR is computed correctly"""

        # Get algorithm parameters
        _, self.curr_parameters = settings.get_parameters()

        # Enable zero padding
        if self.curr_parameters[IDX_ZERO_PADDING] != 1.0:
            settings.change_parameters(IDX_ZERO_PADDING, 1)

        # Time vector
        t = np.arange(600) * 0.1

        # Test signal with variable frequency and 10 Hz sampling frequency
        for n in range(0, 25):
            frequency = np.random.uniform(0.8, 1.5, 1)
            phase = np.random.rand(1) - 0.5
            signal = np.cos(2 * np.pi * t * frequency + phase)
            yield self.compute_heart_rate_frequency, signal, frequency

        # Undo changes
        if self.curr_parameters[IDX_ZERO_PADDING] != 1.0:
            settings.change_parameters(IDX_ZERO_PADDING, 0)

    def compute_heart_rate_frequency(self, signal, frequency):
        """Called by test generators in test_compute_heart_rate_frequency"""

        # Compute heart rate frequency using algorithm
        ret_1, ret_2, ret_3, ret_4 = self.signal_processor.compute_heart_rate(signal, 10)

        # Using delta because due to limited number of sample we will never equal to frequency
        assert_almost_equal(ret_1, frequency * 60, delta=1)

    def test_estimate_trigger_frequency(self):
        """Test if HR is computed correctly during MRI triggering algorithm"""

        # Test signal with fixed frequency of 1 Hz (60bpm) and 10 Hz sampling frequency
        t = np.arange(600) * 0.1
        signal = np.cos(2 * np.pi * t)

        # Compute heart rate frequency using algorithm
        ret_1, ret_2, ret_3, ret_4, ret_5 = self.signal_processor.estimate_trigger(signal, 10, np.inf)
        assert_equal(ret_1, 60)

    def test_estimate_trigger_phase(self):
        """Test if trigger is computed correctly during MRI triggering algorithm"""

        # Time vector
        t = np.arange(600) * 0.1

        # Test signal with fixed frequency of 1 Hz (60bpm), 10 Hz sampling frequency, and variable phase
        for n in range(0, 50):
            phase = np.random.rand(1) - 0.5
            signal = np.cos(2 * np.pi * t + phase)
            yield self.estimate_trigger_phase, signal, phase

    def estimate_trigger_phase(self, signal, phase):
        """Called by test generators in test_estimate_trigger_phase"""

        # Compute results
        self.signal_processor.estimate_trigger(signal, 10, np.inf)

        if phase > 0:
            assert_almost_equal(self.signal_processor.delta, 1 - np.abs(phase / (2 * np.pi)))
        else:
            assert_almost_equal(self.signal_processor.delta, np.abs(phase / (2 * np.pi)))

    def test_compute_heart_rate_without_zero_padding_data_types(self):
        """Test if data types returned by compute_heart_rate() are valid"""

        ret_1, ret_2, ret_3, ret_4 = self.signal_processor.compute_heart_rate(np.random.rand(100),
                                                                              np.random.randint(10) + 10)
        assert_is_instance(ret_1, float)
        assert_is_instance(ret_2, np.ndarray)
        assert_is_instance(ret_3, np.ndarray)
        assert_is_instance(ret_4, int)

    def test_compute_heart_rate_with_zero_padding_data_types(self):
        """Test if data types returned by compute_heart_rate() are valid"""

        settings.flip_setting(IDX_ZERO_PADDING)

        ret_1, ret_2, ret_3, ret_4 = self.signal_processor.compute_heart_rate(np.random.rand(100),
                                                                              np.random.randint(10) + 10)
        assert_is_instance(ret_1, float)
        assert_is_instance(ret_2, np.ndarray)
        assert_is_instance(ret_3, np.ndarray)
        assert_is_instance(ret_4, int)

        settings.flip_setting(IDX_ZERO_PADDING)


if __name__ == '__main__':
    nose.main()
