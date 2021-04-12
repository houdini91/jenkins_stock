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

build: 
	@docker build . -t stock_analyzer

clean:
	@rm -rf ${TOP_LEVEL}/tmp

run:
	@docker run -it stock_analyzer:latest

.PHONY: start stop status restart clean build test testwarn migrate fixtures cli tail