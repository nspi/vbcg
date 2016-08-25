#!/usr/bin/env python
# -*- coding: ascii -*-
"""signal_processing.py - a class for signal processing"""

import numpy as np
from scipy.optimize import curve_fit


def normalize(inputSignal):
    """Normalize the signal to lie between 0 and 1"""

    outputSignal = inputSignal

    # Prohobit dividing by zero
    if np.max(np.abs(outputSignal)) > 0:
        maxVal = np.max(np.abs(outputSignal))
        minVal = np.min(np.abs(outputSignal))
        # MinMax normalization
        outputSignal = (outputSignal-minVal)/(maxVal-minVal)

    return outputSignal


def curveFitFunc(x, a, b):
    """"linear curve fit function"""

    return a * x + b


def curveFit(inputSignal1, inputSignal2):
    """perform curve fitting and return slope value"""

    m, ret = curve_fit(curveFitFunc, inputSignal1, inputSignal2)
    return m


def filterWaveform(inputRawSignal, inputOutputSignal, inputMagicNumber):
    """This function filters the video signal and thereby obtains a waveform more similar to pulse oximetry
        as described in:

        Spicher N, Maderwald S, Ladd ME and Kukuk M. High-speed, contact-free measurement of the photoplethysmography
        waveform for MRI triggering Proceedings of the 24th Annual Meeting of the ISMRM, Singapore, Singapore,
        07.05.-13.05.2016.
    """

    RawSignal = inputRawSignal
    OutputSignal = inputOutputSignal
    magic_number = inputMagicNumber

    # Normalize values
    valuesNorm = normalize(RawSignal)

    # Perform pseudo derivation
    valuesNormDiff = np.abs(np.diff(valuesNorm))

    # Apply window
    valuesNormDiffWindow = valuesNormDiff[-magic_number:]

    # Prepare fit
    valuesXdata = np.linspace(0, 1, magic_number)

    # Apply curve fit
    valueM = curveFit(valuesXdata, valuesNormDiffWindow)

    # Get output: Computed signal
    OutputSignal = np.append(OutputSignal, valueM[1])

    return OutputSignal


def computeHR(inputRawSignal, estimatedFPS):
    """This simple algorithm computes the heart rate as described in:

        Spicher N, Maderwald S, Ladd ME and Kukuk M. Heart rate monitoring in ultra-high-field MRI using frequency
        information obtained from video signals of the human skin compared to electrocardiography and pulse oximetry.
        Proceedings of the 49th Annual Conference of the German Society for Biomedical Engineering, Luebeck, Germany,
        16.-18.09.2015.
    """

    # Store signal
    signal = inputRawSignal

    # Store number of elements in signal
    N = np.size(signal)

    # Get FPS of video stream
    fps = estimatedFPS

    # Minimal and maximum HR (30..180 bpm)
    hrMin = 0.5
    hrMax = 3

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

    # Get indices of frequncies between hrMin and hrMax
    limits = limitsIdx[limitsBool.nonzero()]
    limits = limits.astype(int)

    # Get index of maximum frequency in FFT spectrum
    max_val = limits[np.argmax(abs(signalFFT[limits]))]

    # Return HR, spectrum with frequency axis, and found maximum
    return (np.round(freqAxis[max_val] * 60)), abs(signalFFT[limits]), freqAxis[limits], max_val-limits[0]
