# Makefile for splunk_app_pagerduty.
#
# Home:: https://github.com/ampledata/splunk_app_pagerduty
# Author:: Greg Albrecht <mailto:gba@splunk.com>
# Copyright:: Copyright 2012 Splunk, Inc.
# License:: Apache License 2.0
#



.DEFAULT_GOAL := all

all: install_requirements install_gemset librarian_update

install_requirements:
	pip install -r requirements.txt --use-mirrors

build: clean
	tar -X .tar_exclude -zcpf splunk_app_pagerduty.spl ../splunk_app_pagerduty

vagrant_up:
	vagrant up

vagrant: vagrant_up

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

test: all lint flake8 clonedigger nosetests

install:
	vagrant ssh -c 'sudo /opt/splunk/bin/splunk install app /vagrant/splunk_app_pagerduty.spl -update true -auth admin:changeme'
	vagrant ssh -c 'sudo /opt/splunk/bin/splunk restart'

add_input:
	vagrant ssh -c 'sudo /opt/splunk/bin/splunk add monitor /var/log -auth admin:changeme'

generate_events:
	vagrant ssh -c 'logger -t generated ERROR'

clean:
	rm -rf *.egg* build dist *.pyc *.pyo cover doctest_pypi.cfg nosetests.xml \
		pylint.log *.egg output.xml flake8.log output.xml */*.pyc .coverage *.spl


install_gemset:
	rvm gemset import pagerduty.gems

librarian_update:
	librarian-chef update

vagrant_provision:
	vagrant provision

vagrant_destroy:
	vagrant destroy -f

nuke: vagrant_destroy clean all vagrant_up build install add_input
