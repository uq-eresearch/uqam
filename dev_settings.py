"""
Extra Development settings

Will override any default settings if a 'development_mode' file exists.
"""
from default_settings import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geouqam',
        'USER': 'uqam',
        'PASSWORD': 'uqam',
        'HOST': 'localhost',
        'PORT': '',
    },
}

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INSTALLED_APPS += ('debug_toolbar',)


# Debug Toolbar configuration
INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

MEDIA_ROOT = os.path.join(DIRNAME, 'media')

HAYSTACK_WHOOSH_PATH = '/home/uqdayers/whoosh/cat_index'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable Template Caching
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

HTTPS_SUPPORT = False

ARCHIVAL_STORAGE = FileSystemStorage(
        location=MEDIA_ROOT + '/archival',
        base_url=MEDIA_URL + 'archival/')

