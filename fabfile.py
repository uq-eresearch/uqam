from fabric.api import env, local, run, put, cd, prefix

env.user = 'uqdayers'
env.gateway = 'gladys'
env.hosts = ['anthropology']


def uname():
    run('uname -a')

def uat():
    env.hosts = ['anthropology']


def pack():
    local('git archive master | bzip2 > /tmp/uqam.tar.bz2')

def bootstrap():
    pack()
    put('/tmp/uqam.tar.bz2', '/tmp/uqam.tar.bz2')
    depdir = 'test/uqam'
    run('mkdir -p %s' % depdir)
    virtenv = '/home/omad/temp'
    reqfile = 'requirements.txt'
    with cd(depdir):
        run('tar xjf /tmp/uqam.tar.bz2')

        run('%s/bin/pip install --requirement=%s' % (virtenv,reqfile))

        run('./manage.py syncdb')
        run('./manage.py migrate')

def copyimages():
    # something with rsync, probably
    put('images')
    local('rsync')

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

