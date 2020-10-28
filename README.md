# NULP_GlobalLogic

## What is used in this project:
  - python 3.8.3
  - [poetry](https://python-poetry.org) 1.1.4
  - [pyenv](https://github.com/pyenv/pyenv#installation) 1.2.21


## Installation
  1. Create a new directory
  2. Open new terminal there
  3. Enter next command 
  ```
  git clone https://github.com/ostapbodnar/Python_Global_Logic.git
  ```
  4. In that folder create a local interpenter using [pyenv](https://github.com/pyenv/pyenv#installation)  
  ```
  pyenv install 3.8.3
  pyenv local 3.8.3
  pyenv init
  ```
     
  5. Using poetry create a new virtula enviroment and install all requirements  
  ``` poetry use env 3.8 ```
  
 ### Installation of all requirements
 
  To get all requirements open terminal and type:
  ```
  poetry self update
  poetry install
  ```
  
  That's it!  
  Project is ready to run!
