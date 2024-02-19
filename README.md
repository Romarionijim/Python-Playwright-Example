
## Project Description 
* This is a test automation infrastructure project developed by using Python programming langauge and Playwright test automation framework with Pytest for UI end to end testing.
* The project was developed on openHR web platform that is an HR management software.
* The project is still under development and yet not finished. 
## Pre requisites
* Python 3.10 or above installed
* PIP installed
* IDE (Pycharm, VScode)
## Getting started
* to get started with the project - first clone the repo:
    * `git clone https://github.com/Romarionijim/Python-Playwright-Example.git`
* install and create a virtual environment for Python to install relevant dependencies 
    * `pip install virtualenv`
* after installing the virtual environment - create it in the Python-Playwright-Example root directory:
    * on MacOS or Linux. - run:
        * `python3 -m venv .venv`
        * activate it by running:
            * `source .venv/bin/activate`
    * on Windows - run:
        * `python -m venv .venv`
        activate it by running:
            * `.venv/Scripts/activate`
    * to make sure the venv is activate - it should display the ".venv" in parentheses on the left of your terminal like this (.venv) 
    
## Installing dependencies 
* after activating your venv - install dependencies from the requirements.txt file by running:
    * `python install -r requirements.txt`
    * this should install all of the existing dependencies stored in the requirements.txt file

## Running tests
* cd to the tests directory
* to run all tests one by one you can run the following command in your termnial using pytest:
    * type `pytest` and press enter - this will run each test that exist one by one 
* run a specific test file:
    * cd to the relevant test file
    * open terminal and run pytest test-file-name (replace it with the actual test file name) / or you can select the current file in pycharm and click on the play button 
* run a specific test function:
    * cd to the relevant test file and open terminal 
    * run the following command: `pytest test-file-name::test-function-name` (replace these with the actual test file and function names)
* run test based on marks/groups:
    * in this project - test functions are grouped by pytest mark decorators
    * to run a specific mark - run:
        * `pytest -m mark-name` (replace this with the actual mark)
        * this will run each test with this specific mark one by one 
## Running tests in parallel
* In order to run tests in parrallel using xdit (which is already installed in requirement.txt) open terminal and run:
 * `pytest -n auto`
 * you can specify the number of processes you wanna run as well e.g `pytest -n 4`
 * this will run tests in parralell based on the number of processes you provided
## Reports
* This project is using Allure report that are already configured and generated after each test under allure-results directory
* to view reports after a test run - open terminal and run:
    * `allure serve /allure-results`
    * the report will be opened on your local browser 
## CI/CD
* In this project I'm using CI/CD - any code changes you'll push will trigger the github actions pipeline where tests will run and an allure report will get automatically generated and deployed to github pages so you can view the test results directly on github under a domain and you can send the report to anyone without the need to downlaod the report and run allure serve.
* Test results allure report will be uploaded as an artifact after each run anyways so you can download it if you prefer that way (the report is retained up to 30 days after test run)
