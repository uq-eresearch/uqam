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
    sudo yum install libjpeg-turbo-devel libtiff-devel zlib-devel lcms-devel

    git clone https://github.com/uq-eresearch/uqam/


    sudo adduser uqam

## Setting up Python 2.7
https://gist.github.com/hangtwenty/5546945

    sudo yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel \
    libxml2-devel libxslt-devel sqlite sqlite-devel  readline-devel
    sudo yum -y groupinstall "Development tools"

    wget --no-check-certificate http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tar.bz2
    tar xf Python-2.7.5.tar.bz2 
    cd Python-2.7.5
    ./configure --prefix=/usr/local
    make && sudo make altinstall

    wget --no-check-certificate https://pypi.python.org/packages/source/v/virtualenvwrapper/virtualenvwrapper-4.1.1.tar.gz
    wget --no-check-certificate https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz

    cd virtualenv-
    sudo python setup.py install


    sudo -u uqam -s
    echo 'export WORKON_HOME=~/Envs' >> .bashrc # Change this directory if you don't like it
    source $HOME/.bashrc
    mkdir -p $WORKON_HOME
    echo '. /usr/bin/virtualenvwrapper.sh' >> .bashrc
    echo 'export PATH=$PATH:/usr/local/bin' >> .bashrc
    source $HOME/.bashrc

    mkvirtualenv uqam --python=/usr/local/bin/python2.7

    cd uqam

    pip install -r requirements/prod.txt


### Setup nginx services

    sudo yum install nginx
    sudo chkconfig nginx on
    sudo service nginx start



### Setup database (*postgresql*):

    $ sudo yum install postgresql-server
    $ service postgresql initdb
    $ sudo service postgresql start
    $ sudo chkconfig postgresql on

Create user and database for uqam:

    $ sudo -u postgres createuser -S -D -R -P uqam
    $ sudo -u postgres createdb --owner uqam --encoding UTF8 uqam

Allow login with username/password from localhost:

    # modify /var/lib/pgsql/data/pg_hba.conf
    # changing 'ident' to 'md5' for the following two lines
    host    all         all         127.0.0.1/32          md5
    host    all         all         ::1/128               md5

Create database tables:

    $ ./manage.py syncdb --all     # Create database tables
    $ ./manage.py migrate --fake   # Enable migrations updates
    $ ./manage.py createsuperuser  # Create admin user

Prepare static files:

    $ mkdir /home/uqam/public
    $ ./manage.py collectstatic

## Setup Solr for search

    # Install Java
    yum install java-1.7.0-openjdk.x86_64

    # Download and install
    wget http://mirror.rackcentral.com.au/apache/lucene/solr/4.7.0/solr-4.7.0.tgz
    tar xvzf solr-4.7.0.tgz
    sudo mv solr-4.7.0/example/ /opt/solr

Create a user account to run Solr:

    sudo useradd -r -d /opt/solr -M -c "Apache Solr" solr
    sudo chown -R solr:solr /opt/solr/

Copy etc files
    
    cp etc/solr-schema.xml /opt/solr/solr/collection1/conf/schema.xml
    cp etc/init-solr /etc/init.d/solr
    chown root:root /etc/init.d/solr
    chmod +x /etc/init.d/solr

    cp etc/sysconfig-solr /etc/sysconfig/solr

Test run:

    sudo -i -u solr
    java -jar start.jar

Start Solr on boot:
    
    chkconfig solr on


## Further documentation

Is available in `docs/`. It can be compiled to *HTML* by:

    (uqam)$ pip install sphinx
    (uqam)$ cd docs; make html


## References
http://www.erikwebb.net/blog/installing-apache-solr-jetty-rhel-6/