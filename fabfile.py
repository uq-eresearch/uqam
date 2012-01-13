from fabric.api import env, local, run, put, cd, prefix, sudo, settings, get
from fabric.api import lcd, open_shell

env.user = 'django'
env.gateway = 'uqdayers@gladys'
env.hosts = ['anthropology-uat']
env.appname = 'uqam'
env.appdir = '/home/django/uqam'
env.virtenv = '/home/django/env'
env.reqfile = env.appdir + '/requirements.txt'


def upgrade():
    """
    Push the latest code, update all requirements, restart everything
    """
    push()
    reqs()
    _collectstatic()
    _syncdb()
    reload_servers()


def bootstrap():
    push()
    run('virtualenv --no-site-packages %(virtenv)s' % env)
    reqs()

def init_celery():
    put('etc/init-celery.conf', '/tmp/celery.conf')
    put('etc/init-celeryd', '/tmp/celeryd')
    with settings(user='uqdayers'):
        sudo('mv /tmp/celery.conf /etc/default/celeryd')
        sudo('mv /tmp/celeryd /etc/init.d/')
        sudo('chown root.root /etc/init.d/celeryd /etc/default/celeryd')
        sudo('chmod 644 /etc/default/celeryd')
        sudo('chmod 755 /etc/init.d/celeryd')
        sudo('service celeryd restart')

def installsyspackages():
    with settings(user='uqdayers'):
        sudo('yum install openldap-devel openssl-devel')

def reqs():
    """Update the remote virtualenv to newest requirements"""
    with prefix('source %(virtenv)s/bin/activate' % env):
        run('pip install --requirement=%(reqfile)s' % env)

def push():
    """Deploy the newest source to the server"""
    filename = _pack()
    put(filename, filename)
    with cd(env.appdir):
        run('tar xjf %s' % filename)

def _collectstatic():
    _venv('./manage.py collectstatic --noinput')

def _pack():
    filename = '/tmp/uqam.tar.bz2'
    local('git archive master | bzip2 > %s' % filename)
    return filename


def _syncdb():
    """Migrate the remote database to the latest version"""
    _venv('./manage.py syncdb')
    _venv('./manage.py migrate')

def resetcat():
    """DANGER: Wipe/Reset the remote catalogue"""
    _venv('./manage.py reset cat loans condition')
    _venv('./manage.py migrate --fake')

def importcat():
    """Remotely import the catalogue and images"""
    classificationsfile = '/home/django/origdb/ClassificationsNov11.xlsx'
    _venv('./manage.py importcategories %s' % classificationsfile)
    _venv('./manage.py importcat /home/django/origdb cat loans condition')
    _venv('./manage.py importxls /home/django/origdb/Museum.xlsx')

def importimages():
    _venv('./manage.py importmedia /home/django/images')

def copyimages():
    local('rsync -rv %s(imagesdir) django@anthropology-uat:images')

#def importdata(db):
    # Either:
    # - copy from another database
    # - do a fresh import

#    sudo('yum install mdbtools')
#    put(db, '/tmp/db.mdb')
#    run('./manage.py importcat pathtomdb')

def _venv(cmd):
    with cd(env.appdir):
        with prefix('source %(virtenv)s/bin/activate' % env):
            run(cmd)

def reload_servers():
    with settings(user='uqdayers'):
        sudo('service nginx reload')
        sudo('service celeryd reload')
        sudo('initctl stop uqam-gunicorn')
        sudo('initctl start uqam-gunicorn')


def rebuild_index():
    """Rebuild the entire search index"""
    _venv('./manage.py rebuild_index')

def update_index():
    """Update search index"""
    _venv('./manage.py update_index')

def test_upgrade():
    temp_archive = "/tmp/current.tar.gz"
    run('rm -f %s' % temp_archive)
    run('tar czf %s --exclude=media %s uqam.db' %
            (temp_archive, env.appname))
    get(temp_archive, temp_archive)

    with lcd('/tmp'):
        local('rm -rf /tmp/uqam.db /tmp/uqam')
        local('tar xzf %s' % temp_archive)

    filename = _pack()
    with lcd('/tmp/uqam'):
        local('tar xjf %s' % filename)
        local('sed -i -r -e "s/\\/home\\/django/\\/tmp/g" default_settings.py')
        local('./manage.py syncdb')
        local('./manage.py migrate')
        local('sed -i -r -e "s/DEBUG = False/DEBUG = True/g" default_settings.py')
#        local('rm -rf ../public; mkdir -p ../public/static ../public/media')
#        local('./manage.py collectstatic --noinput')
        local('./manage.py runserver 0.0.0.0:8000')

def reset_south():
    local("echo 'delete from south_migrationhistory' | manage.py dbshell")
    local("./manage.py reset --noinput cat loans condition")
    local("./manage.py migrate --fake")

def shell():
    open_shell()

def setup_local_database():
    local()

def docs():
    with lcd('docs'):
        local('make html')
