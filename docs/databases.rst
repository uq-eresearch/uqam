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


Create PostgreSQL Database
--------------------------
Create a new database user::

    $ sudo -u postgres createuser -S -D -R -P uqam

Create the database::

    $ sudo -u postgres createdb --owner uqam --encoding UTF8 uqam

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

Create read only database user::

    sudo -u postgres createuser -S -D -R -P uqam_read

Grant the new user privileges to connect to the database::

    sudo -u postgres psql
    GRANT CONNECT ON DATABASE uqam TO uqam_read;

To be properly secure, the public permissions on the database should be 
changed too, since the read only user can still create tables 

http://stackoverflow.com/questions/760210/how-do-you-create-a-read-only-user-in-postgresql
http://linuxhow-tos.blogspot.com.au/2010/11/read-only-user-in-postgresql.html


Import UQAM Data
----------------
The existing Access database tables must be exported into individual CSV files
to be imported into the new catalogue.

Install the required MDB Tools::

    sudo apt-get install mdbtools

Import the new categories used by the museum::

    ./manage.py importcategories ~/temp/Classifications\ Nov11.xlsx

Note, Open/Libre Office cannot be used to edit dates in .xlsx files
since it uses a different format. Excel must be used.

Export the Access MDB file to CSV files::

    python utils/AccessDump.py \
      ~/FinalMuseumData/Anth\ Mus\ Collection\ Database.MDB ~/FinalMuseumData/

Import the CSV files into the new museum catalogue::

    ./manage.py importcat ~/FinalMuseumData/ cat loans condition

This import leaves some of the PostgreSQL sequences in an incorrect state.

Fix this by running::

    utils/fixsequences.sh

Import extra records from the XLS Spreadsheet::

    ./manage.py importxls ~/FinalMuseumData/New\ Artefact\ Record.xls

Import user accounts::

    fab -H anthropology-uat dumpdata:auth.User
    ./manage.py loaddata /tmp/auth.User.json

PostgreSQL Backup and Restore
-----------------------------
Backup::

    $ pg_dump -h {hostname} -U {user-name} {source_db} -f {dumpfilename.sql}

    pg_dump -h localhost -U uqam uqam -f uqam-dbdump-`date +%F.%H%M`.sql

Restore::

    $ psql -h {hostname} -U {user-name} -d {desintation_db} -f {dumpfilename.sql}


Partial Database Backup and Restore
-----------------------------------
Backup only the auth and mediaman apps::

    pg_dump -a -t "auth_*" -t "mediaman_*" -U uqam uqam -f {partialdump.sql}

Restore the same as a full dump.


Drop Database
-------------
The database can be dropped with::

    sudo -u postgres dropdb uqam
