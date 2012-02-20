.. _development:

Development
===========

The **UQAM Catalogue** is still under active development.

-----------
Source Code
-----------
The project source code is managed using git, and be be cloned using::
   $ git clone git://github.com/omad/uqam/


Tools
-----

Django, vim, postgresql, pip, virtualenv, 


Development Environment
-----------------------

These directions assume we're using Ubuntu 11.11.

Install python virtualenv and create a development virtual environment::

    $ sudo apt-get install python-virtualenv git git-gui
    $ virtualenv --no-site-packages uqam

Checkout the source code from github::

    $ cd uqam
    $ git clone git@github.com:omad/uqam.git

Activate the virtual environment and install all dependencies::

    $ source bin/activate
    $ sudo apt-get install python-dev libldap2-dev libjpeg62-dev \
    libgsasl2-dev zlib1g-dev
    # Extra step for AMD64 ubuntu, weird lib locations
    $ sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/
    $ sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
    $ pip install -r uqam/requirements.txt
    $ pip install -r uqam/requirements_dev.txt

Set to using development settings::

    $ touch uqam/development_mode

Install PostgreSQL database server::

    $ sudo apt-get install postgresql pgadmin3 postgresql-contrib
    


Database Configuration
----------------------
Set a password for accessing postgresql::

    $ sudo -u postgres psql
    postgres=# ALTER ROLE postgres WITH ENCRYPTED PASSWORD 'mypassword';
    \q

    CREATE EXTENSION adminpack;
    CREATE DATABASE 'uqam' WITH ENCODING 'UTF-8';

Python PosgreSQL drivers
------------------------
Install the python postgres drivers into the virtual environment.

First install the ubuntu development packages::

    $ sudo apt-get install libpq-dev

Django Database Setup
---------------------
Check the `dev_settings.py` file that the correct postgres username,
password, and database are configured. Then get django to generate all the
required tables::

    (uqam)$ ./manage.py syncdb --all

Using `--all` creates all tables straight away, ignoring migrations::

    $ ./manage.py migrate --fake

Fixes up the record of migrations.

Run Development Server
----------------------
Once everything is setup, the development server can be run::

    $ ./manage.py runserver



Import Geonames Data
---------------------

Install the django-geonames app::

    $ pip install https://github.com/ramusus/django-geonames/tarball/master

Modify to remove GeoDjango requirements. Remote point and add latitude and
longitude fields, customising the import scripts also.

Download the geonames data::

    $ ./manage.py download_geonames

Compress ready for insertion into database::

    $ ./manage.py compress_geonames

Load into PostgreSQL::

    $ ./manage.py load_geonames


Import UQAM Data
----------------
Import the new categories used by the museum::

    $ ./manage.py importcategories ~/temp/Classifications\ Nov11.xlsx

Export the Access MDB file to CSV files::

Import the CSV files into the new museum catalogue::

    ./manage.py importcat ~/temp/ cat loans condition




Starting Database Migration
---------------------------
Use south to automatically find any changed fields in the models
and create a migration file::

    ./manage.py schemamigration cat --auto

Check what changes have been found, and when ready, run the migration::

    ./manage.py migrate cat

Deployment
----------
Deployment tasks are automated using Fabric. The first step when deploying
is to try a test deployment, which copies down the live code and database,
and attempts to perform the upgrade locally, including code replacement
and database migration. This is performed by running::
    
    fab test_upgrade

The last part of this runs a local dev server so that you can test the
site locally.

If this runs successfully, the live site can be upgraded by running::

    fab upgrade

This exports the current code from the local git repository, so any code
that isn't checked in will not be deployed. This is copied up to the
server, extracted over the existing code, and any database migrations are
run. The live servers are then restarted.
.. _docs:

-------------
Documentation
-------------
The documentation is written in `reStructured Text`_ format.

Requires Sphinx_, which can be installed with::

   $ pip install sphinx

To view the documentation, build it to html by::

   $ cd docs
   $ make html

**Sphinx** will run and output the docs to ``docs/_build/html``.

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org

