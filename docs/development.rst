.. _development:

Development
===========

The **UQAM Catalogue** is still under active development.

-----------
Source Code
-----------
The project source code is managed using git, and be be cloned using::

   git clone git://github.com/omad/uqam/


Tools
-----

Django, vim, postgresql, pip, virtualenv, 


Development Environment
-----------------------

These directions assume we're using Ubuntu 11.11.

Install python virtualenv and create a development virtual environment::

    sudo apt-get install python-virtualenv git git-gui
    virtualenv --no-site-packages uqam

Checkout the source code from github::

    cd uqam
    git clone git@github.com:omad/uqam.git

Activate the virtual environment and install all dependencies::

    source bin/activate
    sudo apt-get install python-dev libldap2-dev libjpeg62-dev \
    libgsasl2-dev zlib1g-dev
    # Extra step for AMD64 ubuntu, weird lib locations
    sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/
    sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
    pip install -r uqam/requirements.txt
    pip install -r uqam/requirements_dev.txt

Set to using development settings::

    touch uqam/development_mode

Install PostgreSQL database server::

    sudo apt-get install postgresql pgadmin3 postgresql-contrib

----------------------
Database Configuration
----------------------
Set a password for accessing postgresql::

    sudo -u postgres psql
    ALTER ROLE postgres WITH ENCRYPTED PASSWORD 'mypassword';

Create a `~/.pgpass` file to aid local database access::

    hostname:port:database:username:password

With Postgresql 9+::

    CREATE EXTENSION adminpack;

Python PosgreSQL drivers
------------------------
Install the python postgres drivers into the virtual environment.

First install the ubuntu development packages::

    sudo apt-get install libpq-dev

Django Database Setup
---------------------
Check the `dev_settings.py` file that the correct postgres username,
password, and database are configured.  Then follow the instructions
in :ref:`databases` to create the database structure and load data.

Run Development Server
----------------------
Once everything is setup, the development server can be run::

    ./manage.py runserver



Starting Database Migration
---------------------------
Use south to automatically find any changed fields in the models
and create a migration file::

    ./manage.py schemamigration cat --auto

Check what changes have been found, and when ready, run the migration::

    ./manage.py migrate cat


.. _docs:

-------------
Documentation
-------------
The documentation is written in `reStructured Text`_ format.

Requires Sphinx_, which can be installed with::

   pip install sphinx

To view the documentation, build it to html by::

   cd docs
   make html

**Sphinx** will run and output the docs to ``docs/_build/html``.

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org

