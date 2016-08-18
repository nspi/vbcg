#!/usr/bin/env python
# signal_processing.py - Class for processing of the signals obtained from the video

import numpy as np
from scipy.optimize import curve_fit


def normalize(inputSignal):
    # Normalize the signal to lie between 0 and 1

    outputSignal = inputSignal

    # Prohobit dividing by zero
    if np.max(np.abs(outputSignal)) > 0:
        maxVal = np.max(np.abs(outputSignal))
        minVal = np.min(np.abs(outputSignal))
        # MinMax normalization
        outputSignal = (outputSignal-minVal)/(maxVal-minVal)

    return outputSignal


def curveFitFunc(x, a, b):
    # linear curve fit function
    return a * x + b


def curveFit(inputSignal1, inputSignal2):
    # perform curve fitting and return slope value

    m, ret = curve_fit(curveFitFunc, inputSignal1, inputSignal2)

    return m

def algorithm1(inputRawSignal,inputOutputSignal,inputMagicNumber):
    # This function computes the algorithm as described in our ISMRM 2016 contribution
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
    OutputSignal = normalize(OutputSignal)
    # Get outpout: Input signal
    valuesRawOutput = valuesNorm

    return valuesRawOutput,OutputSignal

def algorithm2(inputRawSignal,N,fps):
    # This function computes the algorithm as described in our ISMRM 2016 contribution
    hrMin = 0.5
    hrMax = 3

    RawSignal = inputRawSignal
    valuesWin = RawSignal[0:N] * np.hamming(N)

    fout = np.fft.fft(valuesWin)
    x = np.linspace(0, N / fps, N + 1)
    freq = np.fft.fftfreq(len(valuesWin), x[1] - x[0])

    limits_bool = (hrMin < freq) & (hrMax > freq)
    limits_idx = np.linspace(0, N - 1, N)
    limits = limits_idx[limits_bool.nonzero()]
    limits = limits.astype(int)
    max_val = limits[np.argmax(abs(fout[limits]))]

    return (np.round(freq[max_val] * 60))

# Todo: Implement algorithm #3