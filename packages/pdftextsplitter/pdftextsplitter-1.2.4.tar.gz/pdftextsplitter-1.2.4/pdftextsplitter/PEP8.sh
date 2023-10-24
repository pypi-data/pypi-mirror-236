#!/bin/bash

# This script will verify the PEP-8 Clkean-Code standards:
cd ./TextPart/
pylint --rcfile=./.pylintrc ./*.py
