# Makefile for splunk_app_pagerduty.
#
# Home:: https://github.com/ampledata/splunk_app_pagerduty
# Author:: Greg Albrecht <mailto:gba@splunk.com>
# Copyright:: Copyright 2012 Splunk, Inc.
# License:: Apache License 2.0
#



VAGRANT_CMD='/opt/vagrant/bin/vagrant'
TAR_EX='--exclude .git* --exclude local --exclude metadata/local.meta --exclude *.tar --exclude *.gz --exclude *.spl'


init:
	pip install -r requirements.txt --use-mirrors

build:
	tar --exclude=$(TAR_EX) -zcpf splunk_app_pagerduty.spl ../splunk_app_pagerduty

vagrantinit:
	$(VAGRANT_CMD) init
	$(VAGRANT_CMD) box add base http://files.vagrantup.com/lucid64.box

vagrantup:
	$(VAGRANT_CMD) up

vagrant: vagrantinit vagrantup

download_splunk:
	wget -O splunk-4.3.3-128297-linux-2.6-amd64.deb 'http://www.splunk.com/page/download_track?file=4.3.3/splunk/linux/splunk-4.3.3-128297-linux-2.6-amd64.deb&ac=&wget=true&name=wget&typed=releases'

install_splunk:
	$(VAGRANT_CMD) ssh -c 'sudo dpkg -i /vagrant/splunk-4.3.3-128297-linux-2.6-amd64.deb'
	$(VAGRANT_CMD) ssh -c 'sudo /opt/splunk/bin/splunk enable boot-start --answer-yes'

start_splunk:
	$(VAGRANT_CMD) ssh -c 'sudo /opt/splunk/bin/splunk start --answer-yes'

splunk: download_splunk install_splunk start_splunk

lint:
	pylint -f parseable -i y -r y bin/*.py tests/*.py | tee pylint.log

flake8:
	flake8 --exit-zero  --max-complexity 12 bin/*.py tests/*.py | \
		awk -F\: '{printf "%s:%s: [E]%s\n", $$1, $$2, $$3}' | tee flake8.log

pep8: flake8

clonedigger:
	clonedigger --cpd-output .

nosetests:
	nosetests

test: init lint flake8 clonedigger nosetests

install:
	$(VAGRANT_CMD) ssh -c 'sudo /opt/splunk/bin/splunk install app /vagrant/splunk_app_pagerduty.spl -update true -auth admin:changeme'
	$(VAGRANT_CMD) ssh -c 'sudo /opt/splunk/bin/splunk restart'

upgrade: install

add_input:
	$(VAGRANT_CMD) ssh -c 'sudo /opt/splunk/bin/splunk add monitor /var/log -auth admin:changeme'

generate_events:
	$(VAGRANT_CMD) ssh -c 'logger -t generated ERROR'

clean:
	rm -rf *.egg* build dist *.pyc *.pyo cover doctest_pypi.cfg nosetests.xml \
		pylint.log *.egg output.xml flake8.log output.xml */*.pyc
