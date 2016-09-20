#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_settings.py - tests for src/settings.py"""

import nose
import settings
import numpy as np
import os
import os.path

from defines import *

from nose.tools import assert_equal, assert_true


class Test(object):

    def setUp(self):
        # Backup current options
        self.backup_settings, _ = settings.get_parameters()

    def tearDown(self):
        for i in range(0, np.size(self.backup_settings)):
            settings.change_settings(i, self.backup_settings[i])

    def test_flip_parameter(self):

        # Get current settings
        self.curr_settings_before, _ = settings.get_parameters()

        # Flip parameter in settings
        settings.flip_setting(IDX_CURVES)

        # Get new settings
        self.curr_settings_after, _ = settings.get_parameters()

        # Check if value has been changed
        assert_equal(np.abs(self.curr_settings_before[IDX_CURVES] - self.curr_settings_after[IDX_CURVES]), 1)

        # Return original value
        settings.flip_setting(IDX_CURVES)

    def test_change_settings(self):

        # Get current settings
        self.curr_settings_before, _ = settings.get_parameters()

        # Get current value
        curr_value = self.curr_settings_before[IDX_FPS]

        # Change parameter in settings
        settings.change_settings(IDX_FPS, curr_value + 1)

        # Get new value
        self.curr_settings_after, _ = settings.get_parameters()

        # Check if value has been changed
        assert_equal(self.curr_settings_after[IDX_FPS], curr_value + 1)

        # Undo changes
        settings.change_settings(IDX_FPS, curr_value)

    def test_change_parameters(self):
        # Get current settings
        _, self.curr_parameters_before = settings.get_parameters()

        # Get current value
        curr_value = self.curr_parameters_before[IDX_WIN_SIZE]

        # Change parameter in settings
        settings.change_parameters(IDX_WIN_SIZE, curr_value + 1)

        # Get new value
        _, self.curr_parameters_after = settings.get_parameters()

        # Check if value has been changed
        assert_equal(self.curr_parameters_after[IDX_WIN_SIZE], curr_value + 1)

        # Change parameter in settings
        settings.change_parameters(IDX_WIN_SIZE, curr_value)

    def test_determine_if_under_testing(self):
        # Check if currently under testing
        assert_true(settings.determine_if_under_testing())

    def test_enforce_file_not_found(self):
        """Check if settings.py writes settings.ini file if it does not exist"""

        # Backup settings and remove file
        os.rename('src/settings.ini', 'src/settings_backup.ini')
        # Let settings find no file
        settings.get_parameters()
        # Check if file has been written
        ret = os.path.exists('src/settings.ini')
        # Remove file created by settings.py()
        os.remove('src/settings.ini')
        # Restore backup file
        os.rename('src/settings_backup.ini', 'src/settings.ini')

        assert_true(ret)

if __name__ == '__main__':
    nose.main()
