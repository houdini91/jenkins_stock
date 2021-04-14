#
# Copyright (C) Resilience Cyber Security LTD - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
#
# Written by Mikey Strauss <maestro_support@resilience-sec.com>, Sun Dec 20 2020
#
TOP_LEVEL:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

help:
	@echo "Stock analyzer docker"
	@echo "-----------------------"
	@echo "Usage: make <COMMAND>"
	@echo ""
	@echo "COMMAND: "
	@echo "build - Build docker"
	@echo "run - Run docker"
	@echo "clean - Clean resources"

build_image: build_python
	@docker build . -t stock_analyzer

build_python:
	@python3 py_trans_jenkins/setup.py bdist_wheel

develop_python: 
	@python3 py_trans_jenkins/setup.py develop

install_python: 
	@python3 py_trans_jenkins/setup.py install

remove_python: 
	@pip3 uninstall trans_jenkins

clean:
	@rm -rf ${TOP_LEVEL}/tmp
	@rm -rf ${TOP_LEVEL}/py_trans_jenkins/trans_jenkins.egg-info
	@rm -rf ${TOP_LEVEL}/dist
	@rm -rf ${TOP_LEVEL}/build

run:
	@docker run -it stock_analyzer:latest

.PHONY: help build_image build_python develop_python install_python remove_python clean run