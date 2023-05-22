# Requirements

## TC-Python library
The lecture aims to provide a tutorial for high-throughput calculations with the commercial thermochemical library called TC-Python.
Please make sure that you have installed [Thermo-Calc](https://thermocalc.com/) software in your computer with a valid license.

You can install TC-Python in a python environment by using a SDK in Thermo-Calc.
First, make sure that you activate asm_2023 environment.

> conda activate python_asm_2023

Second, install TC-Python via

> pip install <path to the TC-Python folder>/TC_Python-<version>-py3-none-any.whl

The detailed instruction is given here: [Installing TC-python](https://download.thermocalc.com/docs/tc-python/2022b/html/index.html)

Should you have any question. Please contact me via email:
Sunyong Kwon: kwonsATornlDOTgov

## Other partient libraries

Other python libraries such as numpy, pandas, open-mpi, and mpi4py will be used during the lecture.
You can install these libraries by following commands.

For numpy and pandas:

> conda install numpy pandas

For open-mpi:

> conda install -c conda-forge openmpi=4.1.2

For mpi4py:

> conda install -c conda-forge mpi4py
