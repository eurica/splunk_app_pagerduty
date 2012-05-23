#!/usr/bin/env python
"""PagerDuty Splunk Setup REST Handler."""
__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import logging as logger
import os
import shutil

import splunk.admin


class ConfigPagerDutyApp(splunk.admin.MConfigHandler):
    """PagerDuty Splunk Setup REST Handler."""
    def setup(self):
        if self.requestedAction == splunk.admin.ACTION_EDIT:
            self.supportedArgs.addOptArg('service_api_key')

    def handleList(self, confInfo):
        conf = self.readConf('pagerduty')
        if conf is not None:
            for stanza, settings in conf.items():
                for key, val in settings.items():
                    confInfo[stanza].append(key, val)

    def handleEdit(self, confInfo):
        _ = confInfo
        if self.callerArgs.data['service_api_key'][0] in [None, '']:
            self.callerArgs.data['service_api_key'][0] = ''

        self.writeConf('pagerduty', 'service_api', self.callerArgs.data)
        self._installit()

    def _installit(self):
        """Copies pagerduty.py to Splunk's bin/scripts directory."""
        splunk_home = os.environ['SPLUNK_HOME']
        script_src = os.path.join(
            splunk_home, 'etc', 'apps', 'pagerduty', 'bin', 'pagerduty.py')
        script_dest = os.path.join(splunk_home, 'bin', 'scripts')
        logger.info(
            "Copying script_src=%s to script_dest=%s" %
            (script_src, script_dest))
        shutil.copy(script_src, script_dest)


splunk.admin.init(ConfigPagerDutyApp, splunk.admin.CONTEXT_NONE)
