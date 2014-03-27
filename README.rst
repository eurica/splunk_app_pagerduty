PagerDuty Alert - Trigger PagerDuty Incidents from Splunk Alerts.

Usage
=====

Overview:

1. Download & Install `Splunk <http://www.splunk.com/download>`_.
2. Create a `PagerDuty Service Integration API Key`_.
3. Install this App.
4. Set PagerDuty API Key.
5. Enable Alert (below):

.. _`PagerDuty Service Integration API Key`: http://developer.pagerduty.com/documentation/integration/events

Detailed:

Phase I: Install & Configure App:

#. Download & Install Splunk.
#. From Splunk, select Apps and click Find More Apps:
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/find_more_apps.png
#. Search for 'pagerduty':
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/search_apps.png
#. Restart Splunk:
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/restart_splunk.png
#. From Splunk, select Apps and click Manage Apps:
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/find_more_apps.png
#. Locate 'PagerDuty Alerts' and click 'Set up':
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/app_set_up.png
#. Enter your PagerDuty Integration API Key and click Save:
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/service_api_key.png
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/successfully_updated.png

Phase II: Enable Alert:

#. From Splunk, search for a term and click Save As - Alert:
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/new_search.png
#. Pick a name and schedule for the alert:
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/save_as_alert.png
#. Click 'Run a Script' and enter 'pagerduty.py', then click 'Save':
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/run_a_script.png
    .. image:: https://raw.githubusercontent.com/ampledata/pagerduty_alert/develop/docs/alert_has_been_saved.png
#. Enjoy having Splunk Alerts delivered to PagerDuty!


Author
======
`Greg Albrecht <https://github.com/ampledata>`_


Contributors
============
See CONTRIBUTORS.rst


Copyright
=========
Copyright 2014 OnBeep, Inc.


License
=======
Apache License, Version 2.0

See LICENSE
