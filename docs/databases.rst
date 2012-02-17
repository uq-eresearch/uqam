.. _databases:

Databases
=========

Sqlite
------

Sqlite is a simple database library that provides a complete SQL database
inside a single file, without requiring any extra server software to be
configured and running.

Sqlite was originally used for development, being by far the easiest
database to setup and use, and also being very forgiving in terms of
allowable data.

For a production system, it was deemed unsuitable, because it lacks strict
constraints checking of the data.


PostgreSQL
----------

PostgreSQL is a full database server, with all the bells, whistles and
complexity that includes. It will strictly check any data constraints, and
is thus more suitable for our purposes.


Install Devel Package
---------------------
The PostgreSQL development package is required for the python psycopg2
drivers to be installed into the virtual environment. It is install thus::
    
    yum install postgresql-devel


Exporting through Django
------------------------
Export all the data as a json dump. This uses a lot of memory, beware.

    ./manage.py dumpdata --exclude contenttypes > datadump.json

Possibly this is better, use natural keys, instead of ignoring some data::

    ./manage.py dumpdata --natural > datadump.json


Create PostgreSQL Database
--------------------------
Create a new database user::

    $ sudo -u postgres createuser --password uqam
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) n
    Shall the new role be allowed to create more new roles? (y/n) n

Log into the server and create the database::

    $ sudo -u postgres createdb --owner uqam --encoding UTF8 uqam

OR

    $ sudo -u postgres psql template1
    template1=# CREATE DATABASE uqam_new OWNER uqam ENCODING 'UTF8';

Use django to create the database structure, creating it directly without
using migrations::

    ./manage.py syncdb --all

Load the previous database dump::
    ./manage.py loaddata datadump.json

If `loaddata` complains about duplicate contenttype keys, you can clean up
the database by::

    ./manage.py dbshell
    trunctate django_content_type cascade;

Create Read-Only User
---------------------

CREATE ROLE uqam_read PASSWORD 'uqam_read' LOGIN 
  NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;

GRANT CONNECT ON DATABASE uqam TO uqam_read;

To be properly secure, the public permissions on the database should be 
changed too, since the read only user can still create tables 

http://stackoverflow.com/questions/760210/how-do-you-create-a-read-only-user-in-postgresql
http://linuxhow-tos.blogspot.com.au/2010/11/read-only-user-in-postgresql.html




PostgreSQL Backup and Restore
-----------------------------
Backup:  $ pg_dump -h {hostname} -U {user-name} {source_db} -f {dumpfilename.sql}

Restore: $ psql -h {hostname} -U {user-name} -d {desintation_db} -f {dumpfilename.sql}


