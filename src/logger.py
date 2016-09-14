#!/usr/bin/env python
# -*- coding: ascii -*-
"""logger.py - tool for storing logs of the main program"""

import logging


def init():
    logging.basicConfig(filename='data/LOGFILE', level=logging.DEBUG,
                        format='%(asctime)s %(module)s %(levelname)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
