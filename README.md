## PyDead

Utility for searching of unused code in python projects.

![Python Versions](https://img.shields.io/badge/python-3.4%2C3.5%2C3.6-blue.svg)
[![Travis Build](https://travis-ci.org/SrgyPetrov/pydead.svg?branch=master)](https://travis-ci.org/SrgyPetrov/pydead)
[![Coverage Status](https://coveralls.io/repos/github/SrgyPetrov/pydead/badge.svg?branch=master)](https://coveralls.io/github/SrgyPetrov/pydead?branch=master)

## Installation

`pip install pydead`

## Configuration

You can create file `.pydead` in folder you want to check and specify names of files and directories that should be excluded (unix filename pattern matching used) as shown below:

```
[paths]
exclude = *settings*
          test_*
          script_*.py

```

## Usage

Call `pydead` command in folder you want to check.
