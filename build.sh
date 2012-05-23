#!/bin/sh
# Builds Splunk Application Package for PagerDuty App.
#
# Author:: Greg Albrecht <mailto:gba@splunk.com>
# Copyright:: Copyright 2012 Splunk, Inc.
# License:: Apache License 2.0
#


TAR_EX="--exclude .git* --exclude local --exclude metadata --exclude *.tar --exclude *.gz --exclude *.spl --exclude build.sh"

cd ..
tar -zcpf pagerduty.spl pagerduty
ls -al pagerduty.spl
cd -
