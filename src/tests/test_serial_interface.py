#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_serial_interface.py - tests for src/serial_interface.py"""

import nose
import time
import os

from serial_interface import SerialInterface
from nose.tools import assert_false, assert_equal, assert_true


class Test(object):

    def setUp(self):
        # Create instance
        self.serial_interface = SerialInterface("test")

        # Start
        self.serial_interface.start()

    def tearDown(self):
        # Clear instance
        self.serial_interface.clear()

    def test_send_trigger_is_first_trigger_denied(self):
        """Check if first trigger is ignored"""
        time.sleep(1)
        ret_1, ret_2 = self.serial_interface.send_trigger(0)
        assert_false(ret_1)
        assert_equal(ret_2, 0)

    def test_send_trigger(self):
        """Check if trigger is sent to serial port"""

        # Wait for virtual serial port
        time.sleep(1)

        # Send trigger
        self.serial_interface.send_trigger(0)

        # Wait to trigger to be processed
        time.sleep(1)

        # Has the trigger been written to serial port?
        assert_equal(os.read(self.serial_interface.master, 1024), 'T\n')

    def test_run(self):
        """Check if thread functionality works correctly"""

        # Is thread running?
        assert_true(self.serial_interface.is_alive())

        # Stop thread
        self.serial_interface.clear()

        # Wait for thread to shutdown
        time.sleep(1)

        # Is thread still running or has it shut down?
        assert_false(self.serial_interface.is_alive())

    def test_clear(self):
        """Check if if connection to serial port is closed"""

        # Clear thread and close connection
        self.serial_interface.clear()
        assert_true(self.serial_interface.eventProgramEnd.is_set())
        assert_false(self.serial_interface.serial_connection.isOpen())

if __name__ == '__main__':
    nose.main()
