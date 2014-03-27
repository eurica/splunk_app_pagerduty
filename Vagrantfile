# Vagrantfile for Splunk App for Pagerduty.
#
# -*- mode: ruby -*-
# vi: set ft=ruby :
#
# Author:: Greg Albrecht <mailto:gba@onbeep.com>
# Copyright:: Copyright 2012 Splunk, Inc.
# License:: Apache License 2.0
#


Vagrant::Config.run do |config|
  config.vm.box = 'stormbase_200'
  config.vm.box_url = 'https://dl.dropbox.com/u/4036736/stormbase_200.box'
  config.vm.host_name = 'pagerduty'
  config.vm.forward_port 8000, 5180
  config.vm.forward_port 8089, 5189
  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = ['cookbooks']
    chef.roles_path = 'roles'
    chef.add_role('pagerduty')
    chef.json = {
      'splunk' => {
        'server' => {
          'package' => 'splunk-5.0.1-143156-linux-2.6-amd64.deb',
          'download_url' => 'http://download.splunk.com/releases/5.0.1/splunk/linux/splunk-5.0.1-143156-linux-2.6-amd64.deb'
        }
      }
    }
  end
end
