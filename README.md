## PyDead

Utility for searching of unused code in python projects, such as module’s global classes, functions and names.

![Release](https://img.shields.io/github/release/SrgyPetrov/pydead.svg)
![Python Versions](https://img.shields.io/pypi/pyversions/pydead.svg)
[![Travis Build](https://travis-ci.org/SrgyPetrov/pydead.svg?branch=master)](https://travis-ci.org/SrgyPetrov/pydead)
[![Coverage Status](https://coveralls.io/repos/github/SrgyPetrov/pydead/badge.svg?branch=master)](https://coveralls.io/github/SrgyPetrov/pydead?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/107d63b3532b4dada180d08880f622cb)](https://www.codacy.com/app/SrgyPetrov/pydead?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SrgyPetrov/pydead&amp;utm_campaign=Badge_Grade)

## Installation

`pip install pydead`

## Usage

```
Usage: pydead [OPTIONS]

Options:
  -d, --directory TEXT  Directory of your project.
  -e, --exclude TEXT    Exclude files and directories by the given pattern.
                        Unix filename pattern matching used.
  --help                Show this message and exit.
```

## Examples

Search in current directory

`$ pydead`

Search in specific directory

`$ pydead -d directory`

Exclude files and directories

`$ pydead -e '*settings*' -e 'script_*.py'`
