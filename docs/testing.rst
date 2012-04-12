.. _usage:

Testing
=======

Running Tests
-------------

To run all the tests for the project (slow):

    ./manage.py test

To run only the tests for a specific app:

    ./manage.py test <appname>


Preparing Fixtures
------------------
Any tests using the models require data in a database, which is loaded in using
a fixture. The easiest way to create a fixture is to dump a portion of the live
database into a `json` file.

This dump can be performed as follows:

    
