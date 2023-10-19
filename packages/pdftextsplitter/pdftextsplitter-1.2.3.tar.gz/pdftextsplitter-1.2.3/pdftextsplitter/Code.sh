#!/bin/bash

# This script will run the tests and measure code coverage:
cd ./Tests/Scripts/
coverage run --rcfile=.coveragerc -m pytest # Runs statement coverage
# coverage run --branch -m pytest # Runs branch coverage
# coverage report -m > ../Reports/TheReport.txt
# coverage html -d ../Reports/

# Generate outputs:
# cd ../Tools/
# python CodeCoverage.py $1
coverage report -m
