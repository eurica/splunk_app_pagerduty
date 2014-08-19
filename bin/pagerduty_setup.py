#!/usr/bin/env python

"""PagerDuty Splunk Setup REST Handler."""

__author__ = 'Greg Albrecht <gba@onbeep.com>'
__copyright__ = 'Copyright 2014 OnBeep, Inc.'
__license__ = 'Apache License, Version 2.0'


import os
import logging
import shutil

import splunk.admin


class ConfigPagerDutyApp(splunk.admin.MConfigHandler):

    """PagerDuty Splunk Setup REST Handler."""

    def setup(self):
        if self.requestedAction == splunk.admin.ACTION_EDIT:
            self.supportedArgs.addOptArg('api_key')

    def handleList(self, confInfo):
        conf = self.readConf('pagerduty')
        if conf is not None:
            for stanza, settings in conf.items():
                for key, val in settings.items():
                    confInfo[stanza].append(key, val)

    def handleEdit(self, confInfo):
        del confInfo
        if self.callerArgs.data['api_key'][0] in [None, '']:
            self.callerArgs.data['api_key'][0] = ''

        self.writeConf('pagerduty', 'pagerduty_config', self.callerArgs.data)
        install_pagerduty_py(os.environ.get('SPLUNK_HOME'))


def install_pagerduty_py(splunk_home):

    """Copies pagerduty.py to Splunk's bin/scripts directory."""

    script_src = os.path.join(
        splunk_home, 'etc', 'apps', 'splunk_app_pagerduty', 'bin',
        'pagerduty.py')
    script_dest = os.path.join(splunk_home, 'bin', 'scripts')

    logging.info(
        'Copying script_src=%s to script_dest=%s', script_src, script_dest)
    shutil.copy(script_src, script_dest)


if __name__ == '__main__':
    splunk.admin.init(ConfigPagerDutyApp, splunk.admin.CONTEXT_NONE)
