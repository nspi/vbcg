#!/usr/bin/env python
# -*- coding: ascii -*-
"""serial_interface.py - tool for sending trigger to MRI using a device connected via the serial port"""

import logging
import serial
import time
import threading
import settings

from defines import *

class SerialInterface(threading.Thread):
    """This class provides access to a device connected via the serial port"""

    def __init__(self):
        """If possible, connect to serial port"""

        # Get current settings
        curr_settings = settings.get_parameters()

        # Try to establish connection to serial port
        try:

            self.serial_connection = serial.Serial('/dev/ttyUSB0', 9600)

            self.serial_connection_established = True

        except serial.SerialException:

            self.serial_connection_established = False

            if curr_settings[IDX_TRIGGER]:
                print "Warning: Using a trigger device is enabled but it is not connected"

            logging.warning("There is no serial connection to the trigger device")

        # Create events
        self.trigger_event = threading.Event()
        self.eventProgramEnd = threading.Event()

        # Store current time
        self.last_trigger_time = time.time()

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

                print "Send trigger in: "+ str( (self.curr_trigger_time - self.last_trigger_time) + waiting_time)

                # Store waiting time
                self.waiting_time = waiting_time

                # Activate event
                self.trigger_event.set()

    def run(self):
        """Main functionality of thread"""

        while self.eventProgramEnd.is_set() is False:

            # If a application of trigger is desired
            if self.trigger_event.is_set():

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
