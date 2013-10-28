# UQ Anthropology Museum Catalogue

UQAM is a web-based catalogue used by the University of Queensland Anthropology Museum.

It has a public front end for people to browse the museum's holdings, including photographs, documents, maps and information on the people involved. As well, it provides tools for museum staff to manage the items in the museum, and import any related data.

It is developed using the [Python][] [Django][] web framework.

This software was developed by the [eResearch Group][eResearch] at [The University of Queensland][uq] with funding from ANDS. It is copyright The University of Queensland.

  [Python]: http://www.python.org/
  [Django]: https://www.djangoproject.com/
  [eResearch]: http://www.itee.uq.edu.au/eresearch
  [uq]: http://www.uq.edu.au/

## Development Setup (with Ubuntu)

Install system requirements:

    $ sudo apt-get update
    $ sudo apt-get install virtualenvwrapper git python-dev libldap2-dev \
      libjpeg62-dev postgresql postgresql-contrib libpq-dev
    $ sudo apt-get install libgraphicsmagick++1-dev libboost-python-dev \
      libsasl2-dev

Clone the code from git:

    $ git clone https://github.com/uq-eresearch/uqam.git
    $ cd uqam

Create a python virtual environment:

    $ mkvirtualenv uqam

*If this fails, try logging out and logging in to enable virtualenvwrapper.*

To re-enable the virtual environment later:

    $ workon uqam

Install python dependencies (*both dev and core*):

    (uqam)$ pip install -r requirements_dev.txt -r requirements.txt

Setup database (*postgresql*):

    $ sudo -u postgres createuser -S -D -R -P uqam
    $ sudo -u postgres createdb --owner uqam --encoding UTF8 uqam

Create database tables:

    $ ./manage.py syncdb --all     # Create database tables
    $ ./manage.py migrate --fake   # Enable migrations updates
    $ ./manage.py createsuperuser  # Create admin user

Enable development settings file:

    $ touch development_mode

Run test server:

    $ ./manage.py runserver 0.0.0.0:8000


## Deployment on Red Hat (or compatible distribution)

More details coming soon. For now refer to `fabfile.py` and `docs/`.

http://www.nginxtips.com/how-to-install-nginx-on-centos-rhel/

http://www.tecmint.com/how-to-enable-epel-repository-for-rhel-centos-6-5/
## RHEL/CentOS 6 64-Bit ##

wget http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -ivh epel-release-6-8.noarch.rpm

wget http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm
sudo rpm -Uvh nginx-release-centos-6-0.el6.ngx.noarch.rpm 



sudo yum install postgresql-devel openldap-devel openssl-devel gcc-c++ GraphicsMagick-c++-devel boost-devel ghostscript ghostscript-devel git

git clone https://github.com/uq-eresearch/uqam/


sudo adduser uqam



## Further documentation

Is available in `docs/`. It can be compiled to *HTML* by:

    (uqam)$ pip install sphinx
    (uqam)$ cd docs; make html

