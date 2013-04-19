# UQ Anthropology Museum Catalogue

UQAM is a web-based catalogue used by the University of Queensland Anthropology Museum.

This software is copyright The University of Queensland

## Running Locally (with Ubuntu)

Install system requirements:

    sudo apt-get update
    sudo apt-get install virtualenvwrapper git python-dev libldap2-dev \
      libjpeg62-dev postgresql postgresql-contrib libpq-dev
    sudo apt-get install libgraphicsmagick++1-dev libboost-python-dev \
      libsasl2-dev

Clone from git:

    git clone https://github.com/uq-eresearch/uqam.git

Create virtual environment for python dependencies:

    mkvirtualenv uqam

If this fails, try logging out and logging in to enable
virtualenvwrapper.

Can be activated later with:

    workon uqam


Install python dependencies:

    pip install -r requirements_dev.txt -r requirements.txt

Setup database:

Create database tables:

Use development settings file:

    touch development_mode

Run test server:





## Installing on Red Hat Linux (or compatible distribution)



