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