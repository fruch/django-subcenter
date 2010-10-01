# Django settings for sub project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
#a define to know it's a test system
TEST_SITE = os.name == 'nt'
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
if TEST_SITE:
    DATABASES = {
        'default': {
            'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '../sub.db3', # Or path to database file if using sqlite3.
        }
    }
    SERV_STATIC = True
else:
    DATABASES = {
    'default': {
        'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fruch_sub', # Or path to database file if using sqlite3.
        'USER': 'fruch',                      # Not used with sqlite3.
        'PASSWORD': 'israeL',                  # Not used with sqlite3.
        'HOST': 'mysql.alwaysdata.com',          # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
       }
    }
    SERV_STATIC = False


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'
_ = lambda s: s

LANGUAGES = [('en', _('English')), # id=1
             ('he', _('Hebrew')),  # id=2
             ('ru', _('Russian')),  # id=3
             ]

DEFAULT_LANGUAGE = 1

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'public/site_media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

AUTH_PROFILE_MODULE = 'profiles.Profile'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g_bz8f3x4#gri(1vjnrj8dfi5!&+qi&rt21-$%ii*nhku!olac'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'flags.loaders.filesystem.load_template_source',
    'flags.loaders.app_directories.load_template_source',

#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.locale.LocaleMiddleware'
)

ROOT_URLCONF = 'sub.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
    os.path.join(PROJECT_PATH, 'common-apps/templates'),
)

INSTALLED_APPS = (

    # django internals
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.comments',
   
    # main application code
    'shows',
    'movies',
    'persons',
    'profiles',
    'subtitles',
    'search',
    
    # third partys    
    'djapian',
    'userprofile',
    'utils',
    'rosetta',
    'transmeta',
    'tagging',
    'djcelery',
    'ghettoq',
    'flags',
    'south',
    'photologue',
    'pressroom',
  # debugging tools
    'debug_toolbar',
    'django_nose',

)

I18N_URLS = True
DEFAULT_AVATAR = os.path.join(MEDIA_ROOT, 'generic.jpg')
AVATAR_WEBSEARCH = False

FORCE_LOWERCASE_TAGS = True

DJAPIAN_DATABASE_PATH = os.path.join(PROJECT_PATH, 'djapian_spaces')

INTERNAL_IPS = ('127.0.0.1',)
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
DEBUG_TOOLBAR_CONFIG = { 'INTERCEPT_REDIRECTS':False,
}
TEST_RUNNER = 'utils.test_runner.MyTestRunner'

CARROT_BACKEND = "ghettoq.taproot.Database"
LOG_FILE= os.path.join(PROJECT_PATH, 'sub.log')
LOG_LEVEL = 'warning'
FLAGS_I18N_PREFIX = '/i18n/'
FLAGS_URL = MEDIA_URL
