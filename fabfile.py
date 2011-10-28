from fabric.api import env, local, run, put, cd, prefix

env.user = 'django'
env.gateway = 'uqdayers@gladys'
env.hosts = ['anthropology-uat']
env.appdir = '/home/django/app'
env.virtenv = '/home/django/env'
env.reqfile = env.appdir + '/requirements.txt'




def pack():
    local('git archive master | bzip2 > /tmp/uqam.tar.bz2')

def bootstrap():
    updatesource()


    run('virtualenv --no-site-packages %(virtenv)s' % env)

    with prefix('source %(virtenv)s/bin/activate' % env):
        run('pip install --requirement=%(reqfile)s' % env)

def updatesource():
    pack()
    put('/tmp/uqam.tar.bz2', '/tmp/uqam.tar.bz2')
    with cd(env.appdir):
        run('tar xjf /tmp/uqam.tar.bz2')

def syncdb():
    with cd(env.appdir):
        with prefix('source %(virtenv)s/bin/activate' % env):
            run('./manage.py syncdb')
            run('./manage.py migrate')

def importcat():
    with cd(env.appdir):
        with prefix('source %(virtenv)s/bin/activate' % env):
            run('./manage.py importcat /home/django/origdb')
            run('./manage.py importmedia /home/django/images')

def copyimages():
    # something with rsync, probably
    local('rsync -rv %s(imagesdir) django@anthropology-uat:images')

def importdata(db):
    # Either:
    # - copy from another database
    # - do a fresh import

    sudo('yum install mdbtools')
    put(db, '/tmp/db.mdb')
    run('./manage.py importcat pathtomdb')

def runremote():
    with cd('test/uqam'):
        with prefix('source ../bin/activate'):
            run('./manage.py runserver')

