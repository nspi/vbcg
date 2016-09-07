#!/usr/bin/env python
# -*- coding: ascii -*-
"""settings.py - tool for reading/storing settings of the main program"""

import ConfigParser
import io
import numpy as np
import logging
import os

# Standard parameters if no settings.ini is available
std_param = [1, 1, 0, 1, 0, 0, 30, 1, 1]


def get_parameters():
    """Load parameters from configuration file. The first return value is a flag and true if everything is okay."""

    # Store data from configuration file in array
    param = np.zeros(9)
    parameter_acquired = False

    # Acquire parameters until they are acquired
    while parameter_acquired is False:

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

            # Iterate throughout each option and store them
            i = 0
            for option in options:
                param[i] = config.get('settings', option)
                i += 1

            # Set marker
            parameter_acquired = True

        except IOError:
            logging.warning("Settings file not found! Creating one with standard values.")
            __store_parameters(std_param)

        except:
            logging.warn("Unexpected error when reading configuration. Trying again.")

    # Return parameters
    return param


def flip_parameter(idx):
    """Flip a boolean value in parameters"""

    # Get parameters
    param = get_parameters()

    # Flip boolean value
    param[idx] = 1 - param[idx]

    # Log to file
    tmp_str = "Parameter: %d was changed" % idx
    logging.info(tmp_str)

    # Store in file
    __store_parameters(param)

    # Return parameters
    return param


def change_parameter(idx, val):
    """Change a non-boolean value in parameters"""

    # Get parameters
    param = get_parameters()

    # Change parameter value
    param[idx] = val

    # Store in file
    __store_parameters(param)

    # Return parameters
    return param


def __store_parameters(param):
    """Store parameters in file"""

    parameter_stored = False

    # Acquire parameters until they are acquired
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
            config.set('settings', 'bool_use_webcam', param[0])  # Parameter

            config.set('settings', '# use which camera port?')  # ...
            config.set('settings', 'idx_camera', param[1])  # ...

            config.set('settings', '# use which algorithm?')
            config.set('settings', 'idx_algorithm', param[2])

            config.set('settings', '# Show curves?')
            config.set('settings', 'bool_show_curves', param[3])

            config.set('settings', '# Store frames on hard disk?')
            config.set('settings', 'bool_store_frames', param[4])

            config.set('settings', '# Use viola jones algorithm?')
            config.set('settings', 'bool_use_face_detection', param[5])

            config.set('settings', '# What is the FPS of the camera?')
            config.set('settings', 'val_fps', param[6])

            config.set('settings', '# Which color channel should be used?')
            config.set('settings', 'val_color', param[7])

            config.set('settings', '# Apply zero-padding when using FFT?')
            config.set('settings', 'bool_zero_padding', param[8])

            # Write and close file
            config.write(config_file)
            config_file.close()

            # Set marker
            parameter_stored = True

        except:
            logging.warn("Writing to settings.ini was not successful. Trying again.")

    return 0
