#!/usr/bin/env python
# -*- coding: ascii -*-
"""signal_processing.py - a class for signal processing"""

import numpy as np
import datetime


class SignalProcessor:
    """This class provides the essential signal processing algorithms"""

    def __init__(self):

        # Define variables for function filterWaveform()
        self.valueLastRunningMax = 0
        self.counterRunningMax = 0

        # Get time for filterWaveform() algorithm
        self.currTime = datetime.datetime.now()

    def filterWaveform(self, inputRawSignal, inputOutputSignal, inputParam1, inputParam2, inputParam3):
        """This function filters the video signal and thereby obtains a waveform more similar to pulse oximetry.
           This is a real-time implementation of the algorithm described in:

           Spicher N, Maderwald S, Ladd ME and Kukuk M. High-speed, contact-free measurement of the photoplethysmography
           waveform for MRI triggering Proceedings of the 24th Annual Meeting of the ISMRM, Singapore, Singapore,
           07.05.-13.05.2016.

           inputParam1: Number of preceding values used for filtering (standard value: 9)
           inputParam2: Number of times the running maximum signal has to be stable (standard value: 3)
           inputParam3: Minimum time (in sec) until a new trigger can be sent (standard value: 0.5)

           Please note that the curve fit is at the moment no performed with Gaussian weights.
        """

        # Get signals
        RawSignal = inputRawSignal
        OutputSignal = inputOutputSignal

        # Normalize values
        valuesNorm = self.normalize(RawSignal)

        # Perform pseudo-derivation
        valuesNormDiff = np.abs(np.diff(valuesNorm))

        # Apply window
        valuesNormDiffWindow = valuesNormDiff[-inputParam1:]

        # Prepare fit
        valuesXdata = np.linspace(0, 1, inputParam1)

        # Apply curve fit
        valueM = self.__curveFit(valuesXdata, valuesNormDiffWindow)

        # Get output: Computed signal
        OutputSignal = np.append(OutputSignal, valueM[0])

        # Apply running max window
        valueRunningMax = np.amax(OutputSignal[-inputParam1:])

        # Increase counter if running max is equal to last value. Otherwise reset counter.
        if valueRunningMax == self.valueLastRunningMax:
            self.counterRunningMax += 1
        else:
            self.counterRunningMax = 0
            self.valueLastRunningMax = valueRunningMax

        # Compute time since last trigger was sent
        self.timeDiff = (datetime.datetime.now()-self.currTime).total_seconds()

        # If the running maximum was stable long enough and enough time has passed, return True
        if self.counterRunningMax == inputParam2 and self.timeDiff>inputParam3:

            # Reset counter
            self.counterRunningMax = 0

            # Reset time
            self.currTime = datetime.datetime.now()

            return True, OutputSignal

        else:
            return False, OutputSignal

    def computeHR(self, inputRawSignal, estimatedFPS):
        """This simple algorithm computes the heart rate as described in:

        Spicher N, Maderwald S, Ladd ME and Kukuk M. Heart rate monitoring in ultra-high-field MRI using frequency
        information obtained from video signals of the human skin compared to electrocardiography and pulse oximetry.
        Proceedings of the 49th Annual Conference of the German Society for Biomedical Engineering, Luebeck, Germany,
        16.-18.09.2015.

        Please note that the different length of the input signal N and that a moving average filter as described in
        section 2.4) of the reference is not applied.
        """

        # Get normalized signal
        signal = self.normalize(inputRawSignal)

        # Store number of elements in signal
        N = np.size(signal)

        # Store FPS of video stream
        fps = estimatedFPS

        # Parameters: Minimal and maximum HR (48..180 bpm)
        hrMin = 0.5
        hrMax = 3

        # Todo: Add zero padding as an option in future release
        # Compute next power of 2 from N
        # nextN = self.nextpow2(N)

        # Zero padding: Fill before and after signal with zeros
        # numberBefore, numberAfter = self.computeZeroPaddingValues(nextN - N)
        # signal = np.concatenate((np.zeros(numberBefore), signal, np.zeros(numberAfter)), 0)

        # Use new N value instead
        # N = nextN

        # Use Hamming window on signal
        valuesWin = signal[0:N] * np.hamming(N)

        # Compute FFT
        signalFFT = np.fft.fft(valuesWin)

        # Compute frequency axis
        x = np.linspace(0, N / fps, N + 1)
        freqAxis = np.fft.fftfreq(len(valuesWin), x[1] - x[0])

        # Get boolean values if values are between hrMin and hrMax
        limitsBool = (hrMin < freqAxis) & (hrMax > freqAxis)
        limitsIdx = np.linspace(0, N - 1, N)

        # Get indices of frequencies between hrMin and hrMax
        limits = limitsIdx[limitsBool.nonzero()]
        limits = limits.astype(int)

        # Get index of maximum frequency in FFT spectrum
        max_val = limits[np.argmax(abs(signalFFT[limits]))]

        # Return HR, spectrum with frequency axis, and found maximum
        return (np.round(freqAxis[max_val] * 60)), abs(signalFFT[limits]), freqAxis[limits], max_val - limits[0]


    def normalize(self, inputSignal):
        """Normalize the signal to lie between 0 and 1"""

        outputSignal = inputSignal

        # Prohibit dividing by zero
        if np.max(np.abs(outputSignal)) > 0:
            maxVal = np.max(np.abs(outputSignal))
            minVal = np.min(np.abs(outputSignal))
            # MinMax normalization
            outputSignal = (outputSignal - minVal) / (maxVal - minVal)

        return outputSignal


    def __curveFit(self, inputSignal1, inputSignal2):
        """perform curve fitting and return slope value"""

        # Todo: Add gaussian weights
        m = np.polyfit(inputSignal1, inputSignal2, 1)

        return m

    def nextpow2(self, number):
        """Simple implementation of MATLAB nextpow2 """
        currValue = 2
        while currValue <= number:
            currValue = currValue * 2
        return currValue

    def computeZeroPaddingValues(self, number):
        """During zero padding, we want to fill zeros before and after signal.
        This function computes the number of zeros"""

        numberOfZerosBeforeSignal = np.floor(number / 2)
        if np.fmod(number, 2) == 1:
            numberOfZerosAfterSignal = numberOfZerosBeforeSignal + 1
        else:
            numberOfZerosAfterSignal = numberOfZerosBeforeSignal

        return numberOfZerosBeforeSignal, numberOfZerosAfterSignal
