from fabric.api import env, local, run

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
