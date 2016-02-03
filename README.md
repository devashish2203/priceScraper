# Price Scraper

Test runner uses
* [nose](https://nose.readthedocs.org/en/latest/)
* [nose-htmloutput](https://pypi.python.org/pypi/nose-htmloutput) : To create a HTML report.

#Requirements

Python 2.7 with the above mentioned packages installed. The requirement.txt file can be used to install the dependecies via pip

# Installation

1. Clone the github repo
2. install required packages 
	`pip install -r "requirements.txt"`


# Running the Tests

1. All the tests can be run with the command

`nosetests -s --with-html --with-xunit`
