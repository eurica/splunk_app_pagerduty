# Makefile for splunk_pagerduty.
#
# Author:: Greg Albrecht <gba@onbeep.com>
# Copyright:: Copyright 2014 OnBeep, Inc.
# License:: Apache License, Version 2.0
# Source:: https://github.com/ampledata/splunk_pagerduty
#



.DEFAULT_GOAL := build

BUNDLE_CMD ?= ~/.rbenv/shims/bundle
BUNDLE_EXEC ?= bundle exec

API_KEY ?= 74a4cdf9c8d94b098c9517c2b48a00ec

SPLUNK_PKG ?= splunk-6.0.3-204106-Linux-x86_64.tgz
SPLUNK_ADMIN_PASSWORD ?= okchanged
SPLUNKWEB_PORT ?= 8100
SPLUNKD_PORT ?= 8189

export VAGRANT_CWD ?= .kitchen/kitchen-vagrant/default-ubuntu-1204/


$(BUNDLE_CMD):
	gem install bundler

bundle_install: $(BUNDLE_CMD)
	bundle install

install_tools: bundle_install install_requirements

install_requirements:
	pip install -r requirements.txt --use-mirrors

build: clean
	@tar -X .tar_exclude -s /\.\.\// -zcf build/splunk_pagerduty.spl ../splunk_pagerduty

lint:
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
		-r n bin/*.py tests/*.py || exit 0

flake8:
	flake8 --max-complexity 12 --exit-zero bin/*.py tests/*.py

pep8: flake8

nosetests:
	nosetests

test: install_tools splunk lint flake8 kitchen_converge nosetests

install: build
	vagrant ssh -c 'sudo /opt/splunk/bin/splunk install app /build/splunk_pagerduty.spl -update true -auth admin:$(SPLUNK_ADMIN_PASSWORD)'
	vagrant ssh -c 'sudo /opt/splunk/bin/splunk restart'

add_input:
	vagrant ssh -c 'sudo /opt/splunk/bin/splunk add monitor /var/log -auth admin:$(SPLUNK_ADMIN_PASSWORD)'

config:
	curl -k -d /splunk_pagerduty/pagerduty_config/pagerduty_config/api_key=$(API_KEY) \
		-u admin:$(SPLUNK_ADMIN_PASSWORD) \
		https://localhost:$(SPLUNKD_PORT)/servicesNS/nobody/splunk_pagerduty/apps/local/splunk_pagerduty/setup

generate_event:
	vagrant ssh -c 'logger -t generated event'

clean:
	@rm -rf *.egg* build/* dist/* *.pyc *.pyo cover doctest_pypi.cfg \
	nosetests.xml *.egg output.xml *.log */*.pyc .coverage *.spl *.tgz

vagrant_up:
	vagrant up

vagrant_provision:
	vagrant provision

vagrant_destroy:
	vagrant destroy -f

kitchen_converge:
	bundle exec kitchen converge

kitchen_destroy:
	bundle exec kitchen destroy

splunk: $(SPLUNK_PKG)
	tar -zxf $(SPLUNK_PKG) --strip-components 4 splunk/lib/python2.7/site-packages/splunk

$(SPLUNK_PKG):
	wget http://download.splunk.com/releases/6.0.3/splunk/linux/$(SPLUNK_PKG)

create_saved_search: generate_event
	curl -k -u admin:$(SPLUNK_ADMIN_PASSWORD) https://localhost:$(SPLUNKD_PORT)/servicesNS/admin/search/saved/searches -d name=splunk_pagerduty_saved_search \
		--data-urlencode search='generated event' -d action.script=1 -d action.script.filename=pagerduty.py \
		-d action.script.track_alert=1 -d actions=script -d alert.track=1 -d cron_schedule='*/5 * * * *' -d disabled=0 -d dispatch.earliest_time=-5m@m \
		-d dispatch.latest_time=now -d run_on_startup=1 -d is_scheduled=1 -d alert_type='number of events' -d alert_comparator='greater than' \
		-d alert_threshold=0
