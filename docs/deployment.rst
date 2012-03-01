Deployment Instructions
=======================

The catalogue will be deployed to a virtual private server running on the gladys eResearch group server. Initially one virtual machine, but two (one production, one testing) when the system is made live. The virtual machine is called anthropology, and is configured with 512Mb of RAM and 15Gb of disk space, which can be increased if required.

Software
--------

`Scientific Linux 6.1 <http://www.scientificlinux.org/>`_ will be the 
operating system. The machine will be 
configured using VMChef_ to setup the system software.

.. _VMChef: https://wiki.metadata.net/Virtual_machines_with_Chef 

nginx_ as the front web server, serving any static content and forwarding 
everything else to the application server.

.. _nginx: http://nginx.net/

Gunicorn_ will be used as the python application server. Yet to be decided is whether it will be installed system wide or just for the application user.

.. _Gunicorn: http://gunicorn.org/

PostgreSQL_ as the database.

.. _PostgreSQL: http://www.postgresql.org/

Fabric_ will be used to automate deployment steps for the catalogue. 
This code will be stored in `fabfile.py`__ in the source code.

.. __: https://github.com/omad/uqam/blob/master/fabfile.py

Pip_ is used to save and install any python dependencies for the project. 
The file `requirements.txt`__ details these.

.. __: https://github.com/omad/uqam/blob/master/requirements.txt

Virtualenv_ is used to create isolated python environments for development and deployment.

.. _Fabric: http://www.fabfile.org/
.. _Pip: http://www.pip-installer.org/
.. _Virtualenv: http://www.virtualenv.org/

Fabric
------

Fabric is a simple python tool for managing remote deployments over ssh, by scripting repetitive tasks. Unfortunately the released versions don't include support for SSH gateways, which are required by our virtual machine setup. A forked version supporting gateways can be installed with:

  pip install -e git+https://github.com/ebolwidt/fabric.git#egg=fabric

More information about this issue can be found in the `fabric issue tracking`_ site.

.. _`fabric issue tracking`: https://github.com/fabric/fabric/issues/38

Setup
-----

An application user will be created for the catalogue to run as and store files under.
This step can be run manually, or using an automated system like Chef_.

Make sure that the fabric config has the correct remote host and user name, and that
ssh keys have been added for the remote user to allow login.

Use Fabric_ to create a virtualenv with all required dependencies and the latest
version of the UQAM code::

  fab -H production bootstrap

.. _Chef: http://www.opscode.com/chef/


Deployment
----------
The :ref:`databases` should be set up on the server.

The local data can be moved to the server using::

    fab push_local_database

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

Images should then be imported with::

    fab importimages


