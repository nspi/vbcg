#!/usr/bin/env python
# logger.py - tool for storing logs of the main program

import logging

def init():
    logging.basicConfig(filename='LOGFILE',level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
