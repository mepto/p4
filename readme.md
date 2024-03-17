# Chess tournament tool

## What it does
Chess tournament tool is an offline tool that lets users follow and update a chess tournament results as it happens

## How to install
1. Clone the repository on your computer.

`git clone https://github.com/mepto/p4.git`

2. Make sure you use python 3.10. Check your python version:

`python --version`

3. Create and activate your virtual environment. The methodology below uses the venv module but you may use your favorite
 virtual environment instead.
* Creation from project root:

`python -m venv <your-virtual-env-name>` 
 
* Activation in Windows:

`<your-virtual-env-name>\Scripts\activate.bat`

* Activation in Linux:

`source <your-virtual-env-name>/bin/activate`

4. Install the dependencies with pip

`pip install -r requirements.txt`

## How to use
1. At project root, to launch the script type

`python main.py`

### Navigation
Use numbers as indicated in the menu(s) displayed in the application to 
navigate and create items, update items or print reports.

## Generate flake8 report

pre-commit and its hooks made sure flake8 errors were caught before each 
commit was made. A report certifying the flake8 compliance can be generated 
from the terminal. 
In the terminal, launch the flake8 command and specify the format (html) as 
well as the name of the directory to create and/or in which to store the report.

`flake8 --format=html --htmldir=_flake-report`
