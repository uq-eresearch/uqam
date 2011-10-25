from fabric.api import env, local, run, put, cd

env.user = 'uqdayers'
env.gateway = 'gladys'
env.hosts = ['anthropology']



def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.
    
    Note:: Fabric (and paramiko) can't forward your SSH agent. 
    This helper uses your system's ssh to do so.
    """

    for h in env.hosts:
        try:
            # catch the port number to pass to ssh
            host, port = h.split(':')
            local('ssh -p %s -A %s "%s"' % (port, host, cmd))
        except ValueError:
            local('ssh -A %s "%s"' % (h, cmd))


def uname():
#    sshagent_run('uname -a')
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
    with cd(depdir):
        run('tar xjf /tmp/uqam.tar.bz2')

        run('./manage.py syncdb')
        run('./manage.py migrate')

def copyimages():
    # something with rsync, probably
    put('images')

def importdata(db):
    # Either:
    # - copy from another database
    # - do a fresh import

    sudo('yum install mdbtools')
    put(db, '/tmp/db.mdb')
    run('./manage.py importcat pathtomdb')
