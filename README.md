## PyDead

Utility for searching of unused code in python projects.

![Release](https://img.shields.io/github/release/SrgyPetrov/pydead.svg)
![Python Versions](https://img.shields.io/pypi/pyversions/pydead.svg)
[![Travis Build](https://travis-ci.org/SrgyPetrov/pydead.svg?branch=master)](https://travis-ci.org/SrgyPetrov/pydead)
[![Coverage Status](https://coveralls.io/repos/github/SrgyPetrov/pydead/badge.svg?branch=master)](https://coveralls.io/github/SrgyPetrov/pydead?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/107d63b3532b4dada180d08880f622cb)](https://www.codacy.com/app/SrgyPetrov/pydead?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SrgyPetrov/pydead&amp;utm_campaign=Badge_Grade)

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
