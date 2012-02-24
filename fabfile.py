from fabric.api import env, local, run, put, cd, prefix, sudo, settings, get
from fabric.api import lcd, open_shell

env.user = 'django'
env.gateway = 'uqdayers@gladys'
#env.hosts = ['anthropology']
env.appname = 'uqam'
env.appdir = '/home/django/uqam'
env.tmpappdir = '/home/django/uqam_tmp'
env.virtenv = '/home/django/env'
env.reqfile = env.appdir + '/requirements.txt'
sudouser = 'uqdayers'


def uname():
    run('uname -a')


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
    """
    Bootstrap a remote UQAM Catalogue installation

    Copy the code into a virtualenv on the server and install all requirements
    """
    run('mkdir -p %(appdir)s' % env)
    push()
    installsyspackages()
    run('virtualenv --no-site-packages %(virtenv)s' % env)
    reqs()
    init_celery()


def init_celery():
    put('etc/init-celery.conf', '/tmp/celery.conf')
    put('etc/init-celeryd', '/tmp/celeryd')
    with settings(user=sudouser):
        sudo('mv /tmp/celery.conf /etc/default/celeryd')
        sudo('mv /tmp/celeryd /etc/init.d/')
        sudo('chown root.root /etc/init.d/celeryd /etc/default/celeryd')
        sudo('chmod 644 /etc/default/celeryd')
        sudo('chmod 755 /etc/init.d/celeryd')
        sudo('service celeryd restart')


def init_gunicorn():
    nginxconf = '/etc/nginx/conf.d/gunicorn.conf'
    initconf = '/etc/init/uqam-gunicorn.conf'

    put('etc/init-gunicorn.conf', '/tmp/init-gunicorn.conf')
    put('etc/nginx-gunicorn.conf', '/tmp/nginx-gunicorn.conf')
    with settings(user=sudouser):
        sudo('mv /tmp/init-gunicorn.conf %s' % initconf)
        sudo('mv /tmp/nginx-gunicorn.conf %s' % nginxconf)
        sudo('chown root.root %s %s' % (nginxconf, initconf))
        sudo('chmod 644 %s %s' % (nginxconf, initconf))


def installsyspackages():
    with settings(user=sudouser):
        sudo('yum install postgresql-devel openldap-devel openssl-devel')


def reqs():
    """Update the remote virtualenv to newest requirements"""
    with prefix('source %(virtenv)s/bin/activate' % env):
        run('pip install --requirement=%(reqfile)s' % env)


def push():
    """
    Deploy the newest source to the server
    """
    filename = _pack()
    put(filename, filename)
    run('rm -rf %(tmpappdir)s' % env)
    run('mv %(appdir)s %(tmpappdir)s' % env)
    run('mkdir -p %(appdir)s' % env)

    with cd(env.appdir):
        run('tar xjf %s' % filename)


def _collectstatic():
    _venv('./manage.py collectstatic --noinput')


def _pack():
    filename = '/tmp/uqam.tar.bz2'
    local('git archive master | bzip2 > %s' % filename)
    return filename


def _syncdb():
    """
    Migrate the remote database to the latest version
    """
    _venv('./manage.py syncdb')
    _venv('./manage.py migrate')


def resetcat():
    """
    DANGER: Wipe/Reset the remote catalogue
    """
    _venv('./manage.py reset cat loans condition')
    _venv('./manage.py migrate --fake')


def importcat():
    """
    Remotely import the catalogue data
    """
    classificationsfile = '/home/django/origdb/ClassificationsNov11.xlsx'
    _venv('./manage.py importcategories %s' % classificationsfile)
    _venv('./manage.py importcat /home/django/origdb cat loans condition')
    _venv('./manage.py importxls /home/django/origdb/Museum.xlsx')


def importimages():
    """
    Remotely import images
    """
    _venv('./manage.py importmedia /home/django/images')


def copyimages():
    local('rsync -rv %s(imagesdir) %(host_string)s:images' % env)

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
    with settings(user=sudouser):
        sudo('service nginx reload')
        sudo('service celeryd reload')
        sudo('initctl stop uqam-gunicorn')
        sudo('initctl start uqam-gunicorn')


def rebuild_index():
    """
    Rebuild the entire remote search index
    """
    _venv('./manage.py rebuild_index')


def update_index():
    """
    Update search index
    """
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
        local('sed -ire "s/DEBUG = False/DEBUG = True/g" default_settings.py')
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


def push_local_database():
    dumpfile = '/tmp/uqam_dump.sql.gz'

    local('pg_dump --clean -h localhost -U uqam uqam | '
            ' gzip -c > %s' % dumpfile)
    put(dumpfile, dumpfile)

    run('gunzip -c %s | psql -h localhost -U uqam -d uqam' % dumpfile)


def dumpdata(app):
    filename = '/tmp/%s.json' % app
    _venv('./manage.py dumpdata %s > %s' % (app, filename))
    get(filename, filename)


def loaddata(app):
    filename = '/tmp/%s.json' % app
    put(filename, filename)
    _venv('./manage.py loaddata %s' % filename)


