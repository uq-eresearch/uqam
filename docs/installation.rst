
Installation
============


Create virtualenv

   $ virtualenv --no-site-packages uqam

Grab the code

    $ cd uqam
    $ git clone

Install requirements

    $ pip install -r requirements.txt

Configure database

Create database tables

    $ ./manage.py migrate

Import data
