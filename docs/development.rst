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

    $ sudo apt-get install postgresql pgadmin3
    



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

