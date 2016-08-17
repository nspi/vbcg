#!/usr/bin/env python
# signal_processing.py - Class for processing of the signals obtained from the video

import numpy as np

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
