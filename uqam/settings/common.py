# Bugfix for https://stackoverflow.com/a/39586528/701439
import uuid
uuid._uuid_generate_random = None
# Django settings for uqam project.
import os.path
from utils.secret_key import gen_secret_key

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DJANGO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

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
}

WSGI_APPLICATION = "uqam.wsgi.application"

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
LANGUAGE_CODE = 'en_GB'

# There is only one site
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/srv/uqam-media/'

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

# Additional locations of static files
STATICFILES_DIRS = (
    DJANGO_ROOT + '/static',
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

# Absolute filesystem path to the secret file which holds this project's
# SECRET_KEY. Will be auto-generated the first time this file is interpreted.
SECRET_FILE = os.path.normpath(os.path.join(DJANGO_ROOT, 'deploy', 'SECRET'))

########## KEY CONFIGURATION
# Try to load the SECRET_KEY from our SECRET_FILE. If that fails, then generate
# a random SECRET_KEY and save it into our SECRET_FILE for future loading. If
# everything fails, then just raise an exception.
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        SECRET_KEY = gen_secret_key(50)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Cannot open file `%s` for writing.' % SECRET_FILE)
########## END KEY CONFIGURATION

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

    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'uqam.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    #  or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    DJANGO_ROOT + '/templates',
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
    'subcollections',
    'dataimport',
    'djkombu',
    'parties',
    'common',
    'location',
    'django_tables2',
    'easy_thumbnails',

    'smart_selects',
    'endless_pagination', # don't think this is used...

    'bulkimport'
)

LOGS_ROOT = os.path.join(DJANGO_ROOT, 'logs')
backup_count = 1000
if DEBUG:
    backup_count = 2
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': False,
        },
        #Default handler for everything that we're doing. Hopefully this doesn't double-print
        #the Django things as well. Not 100% sure how logging works :)
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

EMAIL_HOST = 'mail.uq.edu.au'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:8983/solr/collection1',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    }
}

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'uqam.auth.backend.StricterLDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
AUTH_LDAP_SERVER_URI = "ldaps://ldap.uq.edu.au"
import ldap
from django_auth_ldap.config import LDAPSearch
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=people,o=the university of queensland,c=au",
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
    r'/admin/(.*)$',
    r'/accounts/(.*)$',
    r'/mediaman/(.*)$'
)

LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'/accounts/login(.*)$',
    r'/accounts/logout(.*)$',
    r'/admin/logout(.*)$',
    r'/place/kml$',
    r'/$'
)

GRAPPELLI_ADMIN_TITLE = "<a href='/'>UQ Anthropology Museum Catalogue</a>"

import djcelery
djcelery.setup_loader()
BROKER_TRANSPORT = "django"

GRAPPELLI_INDEX_DASHBOARD = 'uqam.grapdashboard.UQAMDashboard'


THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'easy_thumbnails.processors.filters',
    'mediaman.thumbnail_processors.watermark_overlay',
    'mediaman.thumbnail_processors.expand_canvas',
    'mediaman.thumbnail_processors.watermark_processor',
)

# This normally protects against XSS attacks, which shouldn't be a problem here.
# If enabled, it interrupts the bulk upload functionality.
SESSION_COOKIE_HTTPONLY = False

PUBLIC_DOMAIN = 'catalogue.anthropologymuseum.uq.edu.au'
SECURE_DOMAIN = 'catalogue.anthropologymuseum.uq.edu.au'
XSESSION_DOMAINS = ['http://catalogue.anthropologymuseum.uq.edu.au']
HTTPS_SUPPORT = True
SECURE_REQUIRED_PATHS = (
    '/admin/',
    '/accounts/',
    '/chaining/',
    '/grappelli/'
)


from django.core.files.storage import FileSystemStorage
ARCHIVAL_STORAGE = FileSystemStorage(
        location=MEDIA_ROOT + '/archival',
        base_url=MEDIA_URL + 'archival/')


THUMBNAIL_SOURCE_GENERATORS = (
        'easy_thumbnails.source_generators.pil_image',
        'mediaman.source_generators.pgmagick_image',
    )

THUMBNAIL_ALIASES = {
    '': {
        'large_display': {
            'size': (1024, 768),
            'watermark_image': 'watermark-large.png',
            'wm_margin': 15,
        },
        'item_display': {
            'size': (384, 256),
            'watermark_image': 'watermark-small.png',
            'wm_margin': 5,
#            'watermark': 'UQ Anthropology Museum',
            'expand': True

        },
        'small_thumb': {
            'size': (105, 70),
            'expand': True,
        },
        'large_thumb': {
            'size': (180, 120),
            'expand': True,
        },
        'homepage_new_acquisition': {
            'size': (165, 150),
            'crop': False
        }
    }
}


### Testing ###
TEST_RUNNER = "ignoretests.DjangoIgnoreTestSuiteRunner"
IGNORE_TESTS = (
    'django.contrib.auth',
    'django.contrib.messages',
    'easy_thumbnails',
)
