#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Splunk App for PagerDuty."""

__author__ = 'Greg Albrecht <gba@onbeep.com>'
__copyright__ = 'Copyright 2014 OnBeep, Inc.'
__license__ = 'Apache License, Version 2.0'


import os
import random
import time
import unittest

import fabric
import fabtools.vagrant

import requests

# from .context import bin  # pylint: disable=W0622


APP_NAME = 'splunk_app_pagerduty'
SPLUNK_ADMIN_PASSWORD = 'okchanged'
SPLUNKD_PORT = 8189
SPLUNK_HOME = '/opt/splunk'
API_KEY = '74a4cdf9c8d94b098c9517c2b48a00ec'


class TestSplunkPagerDutyApp(unittest.TestCase):  # NOQA pylint: disable=R0902, R0904

    """Tests for splunk_app_pagerduty App."""

    def setUp(self):
        self.auth = "-auth admin:%s" % SPLUNK_ADMIN_PASSWORD
        self.app_path = os.path.join(SPLUNK_HOME, 'etc', 'apps', APP_NAME)
        self.fcontains = fabric.contrib.files.contains
        self.fexists = fabric.contrib.files.exists

    def tearDown(self):
        self.remove_app()
        ss_conf = os.path.join(
            SPLUNK_HOME, 'etc', 'users', 'admin', 'search', 'local',
            'savedsearches.conf'
        )
        with fabtools.vagrant.vagrant_settings():
            fabric.api.sudo("rm -rf %s" % ss_conf)

    @staticmethod
    def randstr(length=8):
        """Generates a random string of `len`."""
        return ''.join(
            [random.choice('unittest0123456789') for _ in range(length)])

    def backup_app(self):
        """Backs up App for post-test forensics."""
        with fabtools.vagrant.vagrant_settings():
            fabric.api.sudo(
                'tar -zcpf /tmp/%s_%s.tgz %s || true' %
                (APP_NAME, time.time(), self.app_path)
            )

    @staticmethod
    def build_app():
        """Builds App archive."""
        fabric.api.local('make clean build')

    # TODO(@ampledata) Not fully implemented yet.
    @staticmethod
    def configure_app(**kwargs):
        """Configures app with given parameters."""
        endpoint = (
            "/servicesNS/nobody/%s/apps/local/%s/setup" % (APP_NAME, APP_NAME))
        config_ns = "/%s/pagerduty_config/pagerduty_config" % APP_NAME
        config_url = "https://localhost:%s%s" % (SPLUNKD_PORT, endpoint)

        config_data = {"%s/api_key" % config_ns: API_KEY}

        return requests.post(
            config_url,
            data=config_data,
            verify=False,
            auth=('admin', SPLUNK_ADMIN_PASSWORD)
        )

    @staticmethod
    def splunk_cmd(cmd_args):
        """
        Runs the given splunk command on the remote host using sudo.

        @param cmd_args: Command and arguments to run with Splunk.
        @type cmd_args: str

        @return: Command results.
        @rtype: `fabric.api.sudo`
        """
        return fabric.api.sudo("%s/bin/splunk %s" % (SPLUNK_HOME, cmd_args))

    @staticmethod
    def splunk_restart():
        """Restarts Splunk."""
        return TestSplunkPagerDutyApp.splunk_cmd('restart')

    def remove_app(self):
        """Removes the App."""
        with fabtools.vagrant.vagrant_settings():
            TestSplunkPagerDutyApp.splunk_cmd(
                "remove app %s %s || true" % (APP_NAME, self.auth)
            )
            TestSplunkPagerDutyApp.splunk_restart()

    def install_app(self):
        """Installs the App."""
        with fabtools.vagrant.vagrant_settings():
            TestSplunkPagerDutyApp.splunk_cmd(
                "install app /build/%s.spl -update true %s" %
                (APP_NAME, self.auth)
            )
            TestSplunkPagerDutyApp.splunk_restart()

    def test_build_app(self):
        """Tests building App archive."""
        TestSplunkPagerDutyApp.build_app()
        self.assertTrue(os.path.exists("build/%s.spl" % APP_NAME))

    def test_install_app(self):
        """Tests installing App."""
        TestSplunkPagerDutyApp.build_app()
        self.install_app()
        with fabtools.vagrant.vagrant_settings():
            self.assertTrue(self.fexists(self.app_path))

    def test_uninstall_app(self):
        """Tests uninstalling App."""
        TestSplunkPagerDutyApp.build_app()
        self.install_app()
        self.remove_app()
        with fabtools.vagrant.vagrant_settings():
            self.assertFalse(self.fexists(self.app_path))

    def test_unconfigured_app(self):
        """Tests that App is not configured upon initial install."""
        self.install_app()

        config_file = "%s/local/pagerduty.conf" % self.app_path
        app_config = "%s/local/app.conf" % self.app_path

        with fabtools.vagrant.vagrant_settings():
            self.assertFalse(
                self.fexists(config_file, use_sudo=True, verbose=True)
            )

            self.assertFalse(
                self.fexists(app_config, use_sudo=True, verbose=True)
            )

    def test_configured_app(self):
        """Tests configuring App."""
        self.install_app()

        endpoint = (
            "/servicesNS/nobody/%s/apps/local/%s/setup" % (APP_NAME, APP_NAME))
        config_ns = "/%s/pagerduty_config/pagerduty_config" % APP_NAME
        config_url = "https://localhost:%s%s" % (SPLUNKD_PORT, endpoint)

        rand_api_key = TestSplunkPagerDutyApp.randstr()

        config_data = {"%s/api_key" % config_ns: rand_api_key}

        config_file = "%s/local/pagerduty.conf" % self.app_path
        app_config = "%s/local/app.conf" % self.app_path

        print "config_url=%s" % config_url
        print "config_data=%s" % config_data

        conf_result = requests.post(
            config_url,
            data=config_data,
            verify=False,
            auth=('admin', SPLUNK_ADMIN_PASSWORD)
        )

        self.assertEqual(200, conf_result.status_code)

        with fabtools.vagrant.vagrant_settings():
            self.assertTrue(
                self.fexists(config_file, use_sudo=True, verbose=True),
                "Config file %s does not exist." % config_file
            )

            self.assertTrue(
                self.fexists(app_config, use_sudo=True, verbose=True),
                "App config %s does not exist." % app_config
            )

            self.assertTrue(
                self.fcontains(
                    app_config,
                    text='is_configured = 1',
                    use_sudo=True
                ),
                'App is not configured.'
            )

            self.assertTrue(
                self.fcontains(
                    config_file,
                    text="api_key = %s" % rand_api_key,
                    use_sudo=True
                )
            )
