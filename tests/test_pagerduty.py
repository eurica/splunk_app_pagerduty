#!/usr/bin/env python
"""Tests for Splunk App for PagerDuty.

Derived from @samuelks' Python Pagerduty Module
https://github.com/samuel/python-pagerduty
"""

__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import ConfigParser
import csv
import gzip
import os
import random
import shutil
import tempfile
import unittest

from .context import bin


class TestPagerDuty(unittest.TestCase):
    """Tests for Splunk Pagerduty App."""

    def setUp(self):
        self.config_file = tempfile.mkstemp()[1]
        self.events_file = tempfile.mkstemp()[1]
        self.rands = ''.join(
            [random.choice('unittest0123456789') for xyz in range(8)])
        self.rand_row = [self.rands, self.rands]

    def _setup_splunk_home(self):
        self.raw_config = 'default/pagerduty.conf'
        self.raw_pagerduty_py = 'bin/pagerduty.py'

        self.splunk_home = tempfile.mkdtemp()

        self.pd_app = os.path.join(
            self.splunk_home, 'etc', 'apps', 'pagerduty')
        self.pd_bin = os.path.join(self.pd_app, 'bin')
        self.pd_default = os.path.join(self.pd_app, 'default')
        self.spl_scripts = os.path.join(
            self.splunk_home, 'bin', 'scripts')

        os.makedirs(self.pd_bin)
        os.makedirs(self.pd_default)
        os.makedirs(self.spl_scripts)

        shutil.copyfile(self.raw_config, self.config_file)
        shutil.copy(self.raw_pagerduty_py, self.pd_bin)

    def test_get_service_api_key(self):
        self._setup_splunk_home()
        config = ConfigParser.RawConfigParser()
        config.read(self.config_file)
        config.set('pagerduty_api', 'service_api_key', self.rands)
        with open(self.config_file, 'wb') as cfg:
            config.write(cfg)
        service_api_key = bin.pagerduty.get_service_api_key(self.config_file)
        self.assertEqual(service_api_key, self.rands)

    def test_extract_events(self):
        gzf = gzip.open(self.events_file, 'wb')
        writer = csv.writer(gzf)
        writer.writerow(self.rand_row)
        gzf.close()

        events = bin.pagerduty.extract_events(self.events_file)
        self.assertTrue(self.rand_row in events.reader)
