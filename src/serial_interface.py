#!/usr/bin/env python
# -*- coding: ascii -*-
"""serial_interface.py - tool for sending trigger to MRI using a device connected via the serial port"""

import serial
import time
import threading
import settings
import numpy as np
import pty
import os
import logging


class SerialInterface(threading.Thread):
    """This class provides access to a device connected via the serial port"""

    def __init__(self, name):
        """If possible, connect to serial port"""

        # If using tests, create virtual serial port
        if settings.determine_if_under_testing():

            self.master, self.slave = pty.openpty()
            self.vPort = os.ttyname(self.slave)
            self.serial_connection = serial.Serial(self.vPort, 9600)
            self.serial_connection_established = True

        # If not under testing, try to open connection to actual serial port
        else:

            # Try to establish connection to serial port
            try:
                self.serial_connection = serial.Serial(name, 9600)
                self.serial_connection_established = True

            # If it fails, use virtual serial port
            except serial.SerialException:

                # Create virtual serial port
                self.master, self.slave = pty.openpty()
                self.vPort = os.ttyname(self.slave)

                # Create instance
                self.serial_connection = serial.Serial(self.vPort, 9600)
                self.serial_connection_established = True

                logging.warn("Trigger device not found -> Using virtual device")

        # Create events
        self.trigger_event = threading.Event()
        self.eventProgramEnd = threading.Event()

        # Store current time
        self.last_trigger_time = time.time()
        self.firstRun = True

        # Call initialization of thread class
        threading.Thread.__init__(self)

    def send_trigger(self, waiting_time):
        """Send command to serial connection after certain time"""

        # If connection on serial port is available
        if self.serial_connection_established:

            # Get current time
            self.curr_trigger_time = time.time()

            # Only send if the last command was sent >0.5 second ago
            if (self.curr_trigger_time - self.last_trigger_time) > 0.5 and (self.trigger_event.is_set() is False):

                # Store waiting time
                self.waiting_time = waiting_time

                # Activate event
                self.trigger_event.set()

                # Return value for plotting, except if it is the first value that is always wrong
                if self.firstRun:

                    self.firstRun = False
                    return False, 0

                else:
                    return True, (self.curr_trigger_time - self.last_trigger_time) + waiting_time

            else:
                return False, (self.curr_trigger_time - self.last_trigger_time) + waiting_time

    def run(self):
        """Main functionality of thread"""

        while self.eventProgramEnd.is_set() is False:

            # If a application of trigger is desired
            if self.trigger_event.is_set() and not np.isnan(self.waiting_time):

                # Wait
                time.sleep(self.waiting_time)

                # Write to serial port
                self.serial_connection.write('T\n')

                # Store current time
                self.last_trigger_time = time.time()

                # Clear event
                self.trigger_event.clear()

            # Sleep so that other threads are not blocked
            time.sleep(0.01)

    def clear(self):
        # End thread
        self.eventProgramEnd.set()

        # Close serial connection
        if self.serial_connection_established:
            self.serial_connection.close()
