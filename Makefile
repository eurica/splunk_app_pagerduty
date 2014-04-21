# Makefile for splunk_pagerduty.
#
# Home:: https://github.com/ampledata/splunk_pagerduty
# Author:: Greg Albrecht <mailto:gba@onbeep.com>
# Copyright:: Copyright 2014 OnBeep, Inc.
# License:: Apache License, Version 2.0
#



.DEFAULT_GOAL := build

BUNDLE_CMD ?= ~/.rbenv/shims/bundle

BUNDLE_EXEC ?= bundle exec

SPLUNK_PKG ?= splunk-6.0.2-196940-Linux-x86_64.tgz


# Bundler itself:

$(BUNDLE_CMD):
	gem install bundler

bundle_install:
	bundle install


install_requirements:
	pip install -r requirements.txt --use-mirrors

build: clean
	tar -X .tar_exclude -s /\.\.\// -zcf splunk_pagerduty.spl ../splunk_pagerduty

lint:
	pylint -r n bin/*.py tests/*.py || exit 0

flake8:
	flake8 --max-complexity 12 --exit-zero bin/*.py tests/*.py

pep8: flake8

nosetests:
	nosetests tests

test: install_requirements splunk_module lint flake8 nosetests

install: build
	vagrant ssh -c 'sudo /opt/splunk/bin/splunk install app /vagrant/splunk_pagerduty.spl -update true -auth admin:okchanged'
	vagrant ssh -c 'sudo /opt/splunk/bin/splunk restart'

add_input:
	vagrant ssh -c 'sudo /opt/splunk/bin/splunk add monitor /var/log -auth admin:okchanged'

generate_events:
	vagrant ssh -c 'logger -t generated ERROR'

clean:
	rm -rf *.egg* build dist *.pyc *.pyo cover doctest_pypi.cfg nosetests.xml \
		pylint.log *.egg output.xml flake8.log output.xml */*.pyc .coverage *.spl *.tgz

vagrant_up:
	vagrant up

vagrant_provision:
	vagrant provision

vagrant_destroy:
	vagrant destroy -f

splunk_module: splunk

splunk: $(SPLUNK_PKG)
	tar -zxf $(SPLUNK_PKG) --strip-components 4 splunk/lib/python2.7/site-packages/splunk

splunk-6.0.2-196940-Linux-x86_64.tgz:
	wget http://download.splunk.com/releases/6.0.2/splunk/linux/$(SPLUNK_PKG)
