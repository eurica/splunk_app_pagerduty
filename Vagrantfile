# Vagrantfile for Splunk App for Pagerduty.
#
# -*- mode: ruby -*-
# vi: set ft=ruby :
#
# Author:: Greg Albrecht <mailto:gba@splunk.com>
# Copyright:: Copyright 2012 Splunk, Inc.
# License:: Apache License 2.0
#


Vagrant::Config.run do |config|
  config.vm.box = 'base'
  config.vm.forward_port 8000, 4160
  config.vm.forward_port 8089, 4169
end
