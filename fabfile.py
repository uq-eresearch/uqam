from fabric.api import env, local, run, put, cd, prefix, sudo, settings

env.user = 'django'
env.gateway = 'uqdayers@gladys'
env.hosts = ['anthropology-uat']
env.appdir = '/home/django/uqam'
env.virtenv = '/home/django/env'
env.reqfile = env.appdir + '/requirements.txt'




def pack():
    local('git archive master | bzip2 > /tmp/uqam.tar.bz2')

def bootstrap():
    push()

    run('virtualenv --no-site-packages %(virtenv)s' % env)

    reqs()

def installsyspackages():
    with settings(user='uqdayers'):
        sudo('yum install openldap-devel openssl-devel')

def reqs():
    """Update the remote virtualenv to newest requirements"""
    with prefix('source %(virtenv)s/bin/activate' % env):
        run('pip install --requirement=%(reqfile)s' % env)

def push():
    """Deploy the newest source to the server"""
    pack()
    put('/tmp/uqam.tar.bz2', '/tmp/uqam.tar.bz2')
    with cd(env.appdir):
        run('tar xjf /tmp/uqam.tar.bz2')
    collectstatic()

def syncdb():
    """Migrate the remote database to the latest version"""
    virtualenv('./manage.py syncdb')
    virtualenv('./manage.py migrate')

def importcat():
    """Remotely import the catalogue and images"""
    virtualenv('./manage.py importcat /home/django/origdb')
    virtualenv('./manage.py importmedia /home/django/images')

def importimages():
    virtualenv('./manage.py importmedia /home/django/images')

def import_xls():
    virtualenv('./manage.py importxls /home/django/origdb/Museum.xlsx')

def copyimages():
    # something with rsync, probably
    local('rsync -rv %s(imagesdir) django@anthropology-uat:images')

#def importdata(db):
    # Either:
    # - copy from another database
    # - do a fresh import

#    sudo('yum install mdbtools')
#    put(db, '/tmp/db.mdb')
#    run('./manage.py importcat pathtomdb')

def virtualenv(cmd):
    with cd(env.appdir):
        with prefix('source %(virtenv)s/bin/activate' % env):
            run(cmd)

def runremote():
    virtualenv('./manage.py runserver')

def collectstatic():
    virtualenv('./manage.py collectstatic')

def reload():
    with settings(user='uqdayers'):
        sudo('service nginx reload')
        sudo('initctl reload uqam-gunicorn')


def rebuild_index():
    """Rebuild the entire search index"""
    virtualenv('./manage.py rebuild_index')

def update_index():
    """Update search index"""
    virtualenv('./manage.py update_index')
