# Django settings for uqam project.
import os.path

DEBUG = False
TEMPLATE_DEBUG = False

DIRNAME = os.path.dirname(__file__)

ADMINS = (
    ('Damien Ayers', 'd.ayers@uq.edu.au'),
)

MANAGERS = ADMINS

RO_DATABASE = 'readonly'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'uqam',
        'USER': 'uqam',
        'PASSWORD': 'uqam',
        'HOST': 'localhost',
        'PORT': '',
    },
    RO_DATABASE: {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'uqam',
        'USER': 'uqam_read',
        'PASSWORD': 'uqam_read',
        'HOST': 'localhost',
        'PORT': '',
    },
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Brisbane'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-AU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/django/public/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/django/public/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Additional locations of static files
STATICFILES_DIRS = (
    DIRNAME + '/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')v4z&afgu6!lzdoiez778vh4gm#h3jrpl5gpz7aj*+*f$qvj%o'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'uqam.middleware.RequireLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'uqam.middleware.ReverseProxyHttpsHeadersMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

ROOT_URLCONF = 'uqam.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    #  or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    DIRNAME + '/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'djcelery',
    'cat',
    'loans',
    'condition',
    'south',
    'django_extensions',
    'mediaman',
    'haystack',
    'gunicorn',
    'uqamcollections',
    'dataimport',
    'djkombu',
    'reports',
    'parties',
    'common',
    'location',
    'django.contrib.flatpages',
    'tinymce',
    'flatpages_tinymce',
    'django_tables2',
    'django_filters',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_HOST = 'mail.uq.edu.au'

FILEBROWSER_DIRECTORY = ''

HAYSTACK_SITECONF = 'cat.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = '/home/django/whoosh/cat_index'

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'uqam.auth.backend.StricterLDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
AUTH_LDAP_SERVER_URI = "ldap://ldap.uq.edu.au"
import ldap
from django_auth_ldap.config import LDAPSearch
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=staff,ou=people,o=the university of queensland,c=au",
    ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail"
    }
AUTH_LDAP_PROFILE_ATTR_MAP = {"home_directory": "homeDirectory"}


SOUTH_TESTS_MIGRATE = False


# So django-jenkins knows what is local code
PROJECT_APPS = (
    'cat',
    'loans',
    'condition'
)

LOGIN_REQUIRED_URLS = (
    r'/(.*)$',
)
LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'/accounts/login(.*)$',
    r'/admin/logout(.*)$',
    r'/place/kml$',
)

GRAPPELLI_ADMIN_TITLE = "<a href='/'>UQ Anthropology Museum Catalogue</a>"

import djcelery
djcelery.setup_loader()
BROKER_TRANSPORT = "django"
#BROKER_HOST = "localhost"
#BROKER_PORT = 5672
#BROKER_USER = "guest"
#BROKER_PASSWORD = "guest"
#BROKER_VHOST = "/"

GRAPPELLI_INDEX_DASHBOARD = 'uqam.grapdashboard.UQAMDashboard'

TINYMCE_DEFAULT_CONFIG = {
        'theme': 'advanced',
        'relative_urls': False,
        }
