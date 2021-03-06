from fabric.api import env, local, run, put, cd, prefix, sudo, settings, get
from fabric.api import lcd, open_shell
from datetime import date

env.user = 'django'
env.gateway = 'uqdayers@gladys'
#env.hosts = ['anthropology']
env.appname = 'uqam'
env.appdir = '/home/django/uqam'
env.logsdir = '/home/django/uqam/logs'
env.tmpappdir = '/home/django/uqam_tmp'
env.virtenv = '/home/django/env'
env.reqfile = env.appdir + '/requirements/prod.txt'
env.sudouser = 'uqdayers'


def uname():
    run('uname -a')


def upgrade(version="master"):
    """
    Push the latest code, update all requirements, restart everything
    """
    backup()
    push(version)
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
    with settings(user=env.sudouser):
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
    with settings(user=env.sudouser):
        sudo('mv /tmp/init-gunicorn.conf %s' % initconf)
        sudo('mv /tmp/nginx-gunicorn.conf %s' % nginxconf)
        sudo('chown root.root %s %s' % (nginxconf, initconf))
        sudo('chmod 644 %s %s' % (nginxconf, initconf))


def installsyspackages():
    with settings(user=env.sudouser):
        sudo('yum install postgresql-devel openldap-devel openssl-devel')

        #required for pgmagick, which is required for pdf thumbnails
        sudo('yum install gcc-c++ GraphicsMagick-c++-devel boost-devel ghostscript ghostscript-devel')


def reqs():
    """Update the remote virtualenv to newest requirements"""
    with prefix('source %(virtenv)s/bin/activate' % env):
        run('pip install --requirement=%(reqfile)s' % env)


def push(version):
    """
    Deploy the newest source to the server
    """
    filename = _pack(version)
    put(filename, filename)
    run('rm -rf %(tmpappdir)s' % env)
    run('mv %(appdir)s %(tmpappdir)s' % env)
    run('mkdir -p %(appdir)s' % env)
    run('mkdir -p %(logsdir)s' % env)

    with cd(env.appdir):
        run('tar xjf %s' % filename)


def _collectstatic():
    _venv('./manage.py collectstatic --noinput')


def _pack(version):
    filename = '/tmp/uqam.tar.bz2'
    local('git archive %s | bzip2 > %s' % (version, filename))
    return filename


def _syncdb():
    """
    Migrate the remote database to the latest version
    """
    _venv('./manage.py syncdb')
    _venv('./manage.py migrate')


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
    local('rsync -rv %(imagesdir)s %(host_string)s:images' % env)


def _venv(cmd):
    with cd(env.appdir):
        with prefix('source %(virtenv)s/bin/activate' % env):
            run(cmd)


def reload_servers():
    with settings(user=env.sudouser):
        sudo('service nginx reload')
        sudo('initctl stop uqam-gunicorn')
        sudo('initctl start uqam-gunicorn')

def stop_servers():
    with settings(user=env.sudouser):
        sudo('stop uqam-gunicorn')
def start_servers():
    with settings(user=env.sudouser):
        sudo('start uqam-gunicorn')


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


def test_upgrade(version="master"):
    temp_archive = "/tmp/current.tar.gz"
    db_dump = '/tmp/uqam_dump.sql.gz'

    run('rm -f %s' % temp_archive)
    run('tar czf %s --exclude=media %s' % (temp_archive, env.appname))
    get(temp_archive, temp_archive)

    run('pg_dump --clean -h localhost -U uqam uqam | '
            ' gzip -c > %s' % db_dump)

    get(db_dump, db_dump)
    local('sudo -u postgres dropdb uqam')
    local('sudo -u postgres createdb --owner uqam --encoding UTF8 uqam')
    local('echo "GRANT CONNECT ON DATABASE uqam TO uqam_read;" | sudo '
            '-u postgres psql')
    local('gunzip -c %s | psql -h localhost -U uqam -d uqam' % db_dump)

    test_upgrade_2(version)


def test_upgrade_2(version):
    filename = _pack(version)
    local('rm -rf /tmp/uqam')
    local('mkdir -p /tmp/uqam')
    with lcd('/tmp/uqam'):
        local('tar xjf %s' % filename)
        local('sed -i -r -e "s/\\/home\\/django/\\/tmp/g" default_settings.py')
        local('./manage.py syncdb')
        local('./manage.py migrate')
        local('sed -ire "s/DEBUG = False/DEBUG = True/g" default_settings.py')
        local('sed -ire "s/HTTPS_SUPPORT = True/HTTPS_SUPPORT = False/g" default_settings.py')
        local('./manage.py runserver 0.0.0.0:8000')


def reset_south():
    local("echo 'delete from south_migrationhistory' | manage.py dbshell")
    local("./manage.py reset --noinput cat loans condition")
    local("./manage.py migrate --fake")


def shell():
    open_shell()


def docs():
    with lcd('docs'):
        local('make html')


def download_live_data(dumpfile='/tmp/uqam_dump.sql.gz'):
    with settings(host_string='django@anthropology'):
        run('pg_dump --clean -h localhost -U uqam uqam | '
                ' gzip -c > %s' % dumpfile)
        get(dumpfile, dumpfile)

    return dumpfile


def grab_live_data():
    dumpfile = download_live_data()

    local('sudo -u postgres dropdb uqam')
    local('sudo -u postgres createdb --owner uqam --encoding UTF8 uqam')
    local('echo "GRANT CONNECT ON DATABASE uqam TO uqam_read;" | sudo '
            '-u postgres psql')
    local('gunzip -c %s | psql -h localhost -U uqam -d'
            'uqam' % dumpfile)


def update_uat_from_live():
    """
    Drops the UAT DB and copies the live DB to it

    Will stop the UAT app server, which should be updated
    and then restarted manually.
    """
#    dumpfile = download_live_data()
    dumpfile='/tmp/uqam_dump.sql.gz'
    with settings(host_string='django@anthropology-uat'):
        put(dumpfile, dumpfile)
        with settings(host_string="%s@anthropology-uat" % env.sudouser):
            stop_servers()
            run('sudo -u postgres dropdb uqam')
            run('sudo -u postgres createdb --owner uqam --encoding UTF8 uqam')
        run('gunzip -c %s | psql -h localhost -U uqam -d uqam' % dumpfile)

        _venv("""echo "UPDATE django_site SET domain='anthropology.metadata.net, name='anthropology.metadata.net;" | ./manage.py dbshell""")




def backup():
    """
    Create a backup of the current code and database
    """
    now = str(date.today())
    filename = 'backups/backup-' + now + '-preupgrade'
    run('mkdir -p backups')
    run('pg_dump --clean -h localhost -U uqam uqam | '
            ' gzip -c > %s.sql.gz' % filename)
    run('tar czf %s.tar.gz uqam' % filename)
