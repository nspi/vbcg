#!/usr/bin/env python
# main.py - the main program

import settings
import logger

# Initialize logging
logger.init()

# Read configuration
parameters = settings.get_parameters()