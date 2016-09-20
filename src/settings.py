#!/usr/bin/env python
# -*- coding: ascii -*-
"""settings.py - tool for reading/storing settings of the main program and algorithm parameters"""

import ConfigParser
import io
import numpy as np
import logging
import os
import sys
import threading

from defines import *

# Standard parameters if no settings.ini is available
std_settings = [VAL_WEBCAM, VAL_CAMERA, VAL_ALGORITHM, VAL_CURVES, VAL_FRAMES, VAL_FACE, VAL_FPS, VAL_COLORCHANNEL]
std_param = [VAL_ZERO_PADDING, VAL_WIN_SIZE, VAL_RUN_MAX, VAL_MIN_TIME]

# Used for synchronization of threads
lock = threading.Lock()


def get_parameters():
    """Load data from configuration file."""

    # Initialize vector for data
    settings = np.zeros(8)
    parameters = np.zeros(4)

    parameter_acquired = False

    # Block thread
    lock.acquire()

    # Get parameters
    try:
        # Open file
        current_location = os.path.dirname(os.path.realpath(__file__))
        current_location_settings = current_location + os.sep + 'settings.ini'
        with open(current_location_settings) as f:
            sample_config = f.read()
        config = ConfigParser.RawConfigParser()
        config.readfp(io.BytesIO(sample_config))

        # Read settings
        options = config.options('settings')

        # Iterate throughout all program settings and store them
        i = 0
        for option in options:
            settings[i] = config.get('settings', option)
            i += 1

        # Read parameter
        options = config.options('parameters')

        # Iterate throughout each all algorithm parameters and store them
        i = 0
        for option in options:
            parameters[i] = config.get('parameters', option)
            i += 1

        # Release thread
        lock.release()

    except IOError:
        logging.warning("Settings file not found! Creating one with standard values.")
        lock.release()
        __store_parameters(std_settings, std_param)

    # Return parameters
    return settings, parameters


def flip_setting(idx):
    """Flip a boolean value in parameters"""

    # Get parameters
    settings, parameters = get_parameters()

    if idx < 8:

        # Flip boolean value
        settings[idx] = 1 - settings[idx]

        # Log to file
        tmp_str = "Program setting: %d was changed" % idx
        logging.info(tmp_str)

        # Store in file
        __store_parameters(settings, parameters)

    else:
        logging.warning("Algorithm parameters can not be modified using this function.")

    # Return parameters
    return settings, parameters


def change_settings(idx, val):
    """Change a non-boolean value in settings or parameters"""

    # Get parameters
    settings, parameters = get_parameters()

    # Change settings value
    settings[idx] = val

    # Store in file
    __store_parameters(settings, parameters)

    # Return parameters
    return settings, parameters


def change_parameters(idx, val):
    """Change a non-boolean value in settings or parameters"""

    # Get parameters
    settings, parameters = get_parameters()

    # Change settings value
    parameters[idx] = val

    # Store in file
    __store_parameters(settings, parameters)

    # Return parameters
    return settings, parameters


def __store_parameters(settings, parameters):
    """Store settings and parameters in file"""

    parameter_stored = False

    # Block thread
    lock.acquire()

    # Get parameters
    while parameter_stored is False:

        try:

            # Open file
            current_location = os.path.dirname(os.path.realpath(__file__))
            current_location_settings = current_location + os.sep + 'settings.ini'
            config_file = open(current_location_settings, 'w')
            config = ConfigParser.ConfigParser(allow_no_value=True)

            # Add content
            config.add_section('settings')

            config.set('settings', '# use webcam or frames from hard disk?')  # Comment
            config.set('settings', 'bool_use_webcam', settings[0])  # Parameter

            config.set('settings', '# use which camera port?')  # ...
            config.set('settings', 'idx_camera', settings[1])  # ...

            config.set('settings', '# use which algorithm?')
            config.set('settings', 'idx_algorithm', settings[2])

            config.set('settings', '# Show curves?')
            config.set('settings', 'bool_show_curves', settings[3])

            config.set('settings', '# Store frames on hard disk?')
            config.set('settings', 'bool_store_frames', settings[4])

            config.set('settings', '# Use viola jones algorithm?')
            config.set('settings', 'bool_use_face_detection', settings[5])

            config.set('settings', '# What is the FPS of the camera?')
            config.set('settings', 'val_fps', settings[6])

            config.set('settings', '# Which color channel should be used?')
            config.set('settings', 'val_color', settings[7])

            config.add_section('parameters')

            config.set('parameters', '# Algorithm 1: Apply Zero padding?')
            config.set('parameters', 'bool_zero_padding', parameters[0])

            config.set('parameters', '# Algorithm 2: Window Size')
            config.set('parameters', 'val_win_size', parameters[1])

            config.set('parameters', '# Algorithm 2: Number of running max values that has to be reached')
            config.set('parameters', 'val_run_max', parameters[2])

            config.set('parameters', '# Algorithm 2: Minimum time until new trigger')
            config.set('parameters', 'val_min_time', parameters[3])

            # Write and close file
            config.write(config_file)
            config_file.close()

            # Set marker
            parameter_stored = True

        except:
            logging.info("Writing to settings.ini was not successful. Trying again.")

    # Release thread
    lock.release()

    return 0


def determine_if_under_testing():
    """This function returns true is we are currently using nosetests"""
    if 'nose' in sys.modules.keys():
        return True
    else:
        return False
