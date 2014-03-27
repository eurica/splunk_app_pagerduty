# Vagrantfile for Splunk App for Pagerduty.
#
# -*- mode: ruby -*-
# vi: set ft=ruby :
#
# Author:: Greg Albrecht <mailto:gba@onbeep.com>
# Copyright:: Copyright 2014 OnBeep, Inc.
# License:: Apache License, Version 2.0
#


Vagrant.configure('2') do |config|
  config.berkshelf.enabled = true
  config.omnibus.chef_version = :latest

  config.vm.box = 'opscode_ubuntu-12.04_chef-latest-1395363298'
  config.vm.box_url = 'https://s3.amazonaws.com/ob-vm-images/opscode_ubuntu-12.04_chef-latest-1395363298.box'

  config.vm.host_name = 'app-vm'
  config.vm.network('forwarded_port', guest: 8000, host: 5180)
  config.vm.network('forwarded_port', guest: 8089, host: 5189)

  config.vm.provision(:chef_solo) do |chef|
    chef.add_recipe('chef-splunk')
    chef.json = {
      'dev_mode' => true,
      'splunk' => {'accept_license' => true, 'is_server' => true}
    }
    chef.data_bags_path = 'data_bags'
  end
end
