#!/usr/bin/env python
"""Splunk App for Pagerduty."""

__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


from .pagerduty import (PagerDutyException, PagerDuty, extract_events,
    trigger_pagerduty, get_pagerduty_api_key)
