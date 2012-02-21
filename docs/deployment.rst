Deployment Instructions
=======================

The catalogue will be deployed to a virtual private server running on the gladys eResearch group server. Initially one virtual machine, but two (one production, one testing) when the system is made live. The virtual machine is called anthropology, and is configured with 512Mb of RAM and 15Gb of disk space, which can be increased if required.

Software
--------

`Scientific Linux 6.1 <http://www.scientificlinux.org/>`_ will be the 
operating system. The machine will be 
configured using Chef_ to setup the system software.

.. _Chef: https://wiki.metadata.net/Virtual_machines_with_Chef 

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
