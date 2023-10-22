# Matrix manipulation helpers
### Changelog

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Test](#test)

## Project Overview
A POC Python library that should help the data scientists to do data transformations, mainly focused on matrix transformations. The functions in the library are developed with vanilla python, but can work with Numpy arrays as well.

## Prerequisites
Project makes use of numpy and Python 3.10.
To start the process one needs to install dependencies listed in requirements.txt

## Project Structure

Project consists of:
1. `src` - folder with usable matrix manipulation functions
    - `helpers` - file containing required functions
    - `decorators` - decorators used fo validation of incoming data (matrix)
    - `classes` - an additional file with custom Matrix class. Main purpose was to practice inheritance, variance, static typing and goose typing.
2. `tests`

## Test
To run the test execute `python3 -m tests.test` in `matrix-manipulation-aharas` folder.