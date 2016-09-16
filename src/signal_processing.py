#!/usr/bin/env python
# -*- coding: ascii -*-
"""signal_processing.py - a class for signal processing"""

import numpy as np
import datetime
import settings
import serial_interface

from defines import *


class SignalProcessor:
    """This class provides the essential signal processing algorithms"""

    def __init__(self):

        # Define variables for function filterWaveform()
        self.value_last_running_max = 0
        self.counter_running_max = 0
        self.time_diff = None

        # Define variables for function estimate_trigger()
        self.delta_times = np.zeros(30)

        # Get time for trigger algorithm
        self.curr_time = datetime.datetime.now()

        # Create serial interface thread:
        if settings.determine_if_under_testing():
            self.serial_interface = serial_interface.SerialInterface('')
        else:
            self.serial_interface = serial_interface.SerialInterface('/dev/ttyUSB0')

        # Start serial interface thread
        self.serial_interface.start()

    def clear(self):
        self.serial_interface.clear()

    def filter_waveform(self, input_raw_signal, input_output_signal, input_param_1, input_param_2, input_param_3):
        """This function filters the video signal and thereby obtains a waveform more similar to pulse oximetry.
           This is a real-time implementation of the algorithm described in:

           Spicher N, Maderwald S, Ladd ME and Kukuk M. High-speed, contact-free measurement of the photoplethysmography
           waveform for MRI triggering Proceedings of the 24th Annual Meeting of the ISMRM, Singapore, Singapore,
           07.05.-13.05.2016.

           inputParam1: Number of preceding values used for filtering (standard value: 9)
           inputParam2: Number of times the running maximum signal has to be stable (standard value: 3)
           inputParam3: Minimum time (in sec) until a new trigger can be sent (standard value: 0.5)

           Please note that the curve fit is computed at the moment without Gaussian weights.
        """

        # Get signals
        raw_signal = input_raw_signal
        output_signal = input_output_signal

        # Normalize values
        values_norm = self.normalize(raw_signal)

        # Perform pseudo-derivation
        values_norm_diff = np.abs(np.diff(values_norm))

        # Apply window
        values_norm_diff_window = values_norm_diff[-input_param_1:]

        # Prepare fit
        values_x_data = np.linspace(0, 1, input_param_1)

        # Apply curve fit
        value_m = self.__curve_fit(values_x_data, values_norm_diff_window)

        # Get output: Computed signal
        output_signal = np.append(output_signal, value_m[0])

        # Apply running max window
        value_running_max = np.amax(output_signal[-input_param_1:])

        # Increase counter if running max is equal to last value. Otherwise reset counter.
        if value_running_max == self.value_last_running_max:
            self.counter_running_max += 1
        else:
            self.counter_running_max = 0
            self.value_last_running_max = value_running_max

        # Compute time since last trigger was sent
        self.time_diff = (datetime.datetime.now() - self.curr_time).total_seconds()

        # If the running maximum was stable long enough and enough time has passed, return True
        if self.counter_running_max == input_param_2 and self.time_diff > input_param_3:

            # Reset counter
            self.counter_running_max = 0

            # Reset time
            self.curr_time = datetime.datetime.now()

            # Send trigger
            self.serial_interface.send_trigger(0)

            return True, output_signal

        else:
            return False, output_signal

    def compute_heart_rate(self, input_raw_signal, estimated_fps):
        """This simple algorithm computes the heart rate as described in:

        Spicher N, Maderwald S, Ladd ME and Kukuk M. Heart rate monitoring in ultra-high-field MRI using frequency
        information obtained from video signals of the human skin compared to electrocardiography and pulse oximetry.
        Proceedings of the 49th Annual Conference of the German Society for Biomedical Engineering, Luebeck, Germany,
        16.-18.09.2015.

        Please note that the different length of the input signal N and that a moving average filter as described in
        section 2.4) of the reference is not applied.
        """

        # Get normalized signal
        signal = self.normalize(input_raw_signal)

        # Store number of elements in signal
        n = np.size(signal)

        # Store FPS of video stream
        fps = estimated_fps

        # Parameters: Minimal and maximum HR (48..180 bpm)
        hr_min = 0.5
        hr_max = 3

        # Get current settings
        curr_settings = settings.get_parameters()

        # Apply zero padding if it is enabled
        if curr_settings[IDX_ZERO_PADDING]:

            # Compute next power of 2 from N
            next_n = self.nextpow2(self.nextpow2(n))

            # Zero padding: Fill before and after signal with zeros
            number_before, number_after = self.compute_zero_padding_values(next_n - n)
            signal = np.concatenate((np.zeros(number_before), signal, np.zeros(number_after)), 0)

            # Use new N value instead
            n = next_n

        # Use Hamming window on signal
        values_win = signal[0:n] * np.hamming(n)

        # Compute FFT
        signal_fft = np.fft.fft(values_win)

        # Compute frequency axis
        x = np.linspace(0, n / fps, n + 1)
        freq_axis = np.fft.fftfreq(len(values_win), x[1] - x[0])

        # Get boolean values if values are between hrMin and hrMax
        limits_bool = (hr_min < freq_axis) & (hr_max > freq_axis)
        limits_idx = np.linspace(0, n - 1, n)

        # Get indices of frequencies between hrMin and hrMax
        limits = limits_idx[limits_bool.nonzero()]
        limits = limits.astype(int)

        # Get index of maximum frequency in FFT spectrum
        max_val = limits[np.argmax(abs(signal_fft[limits]))]

        # Return HR, spectrum with frequency axis, and found maximum
        return (np.round(freq_axis[max_val] * 60)), abs(signal_fft[limits]), freq_axis[limits], max_val - limits[0]

    def estimate_trigger(self, input_raw_signal, estimated_fps):
        """This simple algorithm computes MRI triggers as described in:

        Spicher N, Kukuk M, Ladd ME and Maderwald S. In vivo 7T MR imaging triggered by phase information obtained from
        video signals of the human skin. Proceedings of the 23nd Annual Meeting of the ISMRM, Toronto, Canada,
        30.05.-05.06.2015.
        """

        # Get normalized signal
        signal = self.normalize(input_raw_signal)

        # Store number of elements in signal
        n = np.size(signal)

        # Store FPS of video stream
        fps = estimated_fps

        # Parameters: Minimal and maximum HR (48..180 bpm)
        hr_min = 0.5
        hr_max = 3

        # Use Hamming window on signal
        values_win = signal[0:n] * np.hamming(n)

        # Compute FFT
        signal_fft = np.fft.fft(values_win)

        # Get phase
        signal_phase = np.angle(signal_fft)

        # Compute frequency axis
        x = np.linspace(0, n / fps, n + 1)
        freq_axis = np.fft.fftfreq(len(values_win), x[1] - x[0])

        # Get boolean values if values are between hrMin and hrMax
        limits_bool = (hr_min < freq_axis) & (hr_max > freq_axis)
        limits_idx = np.linspace(0, n - 1, n)

        # Get indices of frequencies between hrMin and hrMax
        limits = limits_idx[limits_bool.nonzero()]
        limits = limits.astype(int)

        # Get index of maximum frequency in FFT spectrum
        max_val = limits[np.argmax(abs(signal_fft[limits]))]

        # Compute time until next maximum in signal
        if signal_phase[max_val] < 0:
            self.delta = np.abs(signal_phase[max_val] / (2 * np.pi * freq_axis[max_val]))
        else:
            self.delta = (1 / freq_axis[max_val]) - np.abs(signal_phase[max_val] / (2 * np.pi * freq_axis[max_val]))

        # If there are enough values
        if np.count_nonzero(input_raw_signal) >= 400:

            ret_1, ret_2 = self.serial_interface.send_trigger(self.delta)

            if ret_1:

                # Drop first value of array and add at end
                self.delta_times = np.delete(self.delta_times, 0)
                self.delta_times = np.append(self.delta_times, ret_2)

        # Return HR and waiting time until next trigger
        return (np.round(freq_axis[max_val] * 60)), abs(signal_fft[limits]), \
            freq_axis[limits], max_val - limits[0], self.delta_times

    def normalize(self, input_signal):
        """Normalize the signal to lie between 0 and 1"""

        output_signal = input_signal

        # Prohibit dividing by zero
        if np.max(np.abs(output_signal)) > 0:
            max_val = np.max(np.abs(output_signal))
            min_val = np.min(np.abs(output_signal))
            # MinMax normalization
            output_signal = (output_signal - min_val) / (max_val - min_val)

        return output_signal

    def __curve_fit(self, input_signal_1, input_signal_2):
        """perform curve fitting and return slope value"""

        # Todo: Add gaussian weights
        m = np.polyfit(input_signal_1, input_signal_2, 1)

        return m

    def nextpow2(self, number):
        """Simple implementation of MATLAB nextpow2() """
        curr_value = 2
        while curr_value <= number:
            curr_value *= 2
        return curr_value

    def compute_zero_padding_values(self, number):
        """During zero padding, we want to fill zeros before and after signal.
        This function computes the number of zeros"""

        number_of_zeros_before_signal = np.floor(number / 2)
        if np.fmod(number, 2) == 1:
            number_of_zeros_after_signal = number_of_zeros_before_signal + 1
        else:
            number_of_zeros_after_signal = number_of_zeros_before_signal

        return number_of_zeros_before_signal, number_of_zeros_after_signal
