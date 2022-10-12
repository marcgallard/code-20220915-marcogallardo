<h3 align="center">code-20220915-marcogallardo</h3>

![Version](https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)
[![python](https://img.shields.io/badge/python-3.10.4-blue.svg?logo=python&labelColor=yellow)](https://www.python.org/downloads/)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/marcgallard/code-20220915-marcogallardo)

<p align="center">
  BMI calculator that takes in JSON data meeting a specified format which is then categorized according to a given JSON table.
</p>

## About code-20220915-marcogallardo

code-20220915-marcogallardo is a BMI calculator designed to accept basic health data of several patients in JSON format which can then be used to determine their BMI, its respective category, and its associated health risk. The JSON schema and BMI table can be modified if guidelines change in the future.

The basic idea is to: 
1. Read in JSON data
2. Validate it matches the given JSON schema
3. Skips and counts invalid samples to later display as part of the script's final results
4. Groups the data according to the provided BMI table's specifications
5. Appends the calculations to each respective valid sample and writes the results to a new JSON file
6. Displays how many people are of a specified BMI category, 'Overweight' by default

Tests are included by default under the 'tests' folder. Sample data is provided within the 'data' folder. The test script can be found as 'tests.py'. The main script is 'groupBMI.py'.

## Prerequisites

- argparse for parsing arguments passed to the script
- jsonschema to make it easy for validating whether JSON data matches a given schema
- Pip to make installation of argparse and jsonschema easy

## Installation

Clone the repo: `git clone https://github.com/marcgallard/code-20220915-marcogallardo.git`

Then run

    pip install argparse    
    
to install argparse, and
    
    pip install jsonschema
    
to install jsonschema.

## Running main script and tests

Assuming the JSON data file, schema, and BMI table are in the folder 'data' (the folder being in the same directory as the script), one can run the script as follows:

    python groupBMI.py --fileLocation data/data.txt --schemaLocation data/schema.txt --tableLocation data/table.txt
    
Testing can be done in a similar fashion, where the associated test files are stored in the 'tests' folder and the folder is in the same directory as the test script:

    python tests.py

## Copyright and license

Code and documentation copyright 2022 under [me](https://github.com/marcgallard). Code released under the [Apache 2.0 License](https://github.com/marcgallard/code-20220915-marcogallardo/blob/master/LICENSE). Documentation released under [Apache](https://www.apache.org/licenses/LICENSE-2.0).
