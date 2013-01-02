# Django settings for {{ project_name }} project.
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': ':memory:',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

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
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
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
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'tests.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'hyperadmin',
    'dockit',
    'dockit.backends.djangodocument',
    'dockitresource',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
]

DOCKIT_BACKENDS = {
    'default': {
        'ENGINE': 'dockit.backends.djangodocument.backend.ModelDocumentStorage',
    },
    'djangodocument': {
        'ENGINE': 'dockit.backends.djangodocument.backend.ModelDocumentStorage',
    },
}

DOCKIT_INDEX_BACKENDS = {
    'default': {
        'ENGINE': 'dockit.backends.djangodocument.backend.ModelIndexStorage',
    },
    'djangodocument': {
        'ENGINE': 'dockit.backends.djangodocument.backend.ModelIndexStorage',
    },
}

try:
    import pymongo
except ImportError:
    pass
else:
    INSTALLED_APPS.append('dockit.backends.mongo')
    DOCKIT_BACKENDS['mongo'] = {
        'ENGINE':'dockit.backends.mongo.backend.MongoDocumentStorage',
        'HOST':'localhost',
        'DB':'testdb',
        'PORT': 27017,
    }
    
    DOCKIT_INDEX_BACKENDS['mongo'] = {
        'ENGINE':'dockit.backends.mongo.backend.MongoIndexStorage',
        'HOST':'localhost',
        'DB':'testdb',
        'PORT': 27017,
    }

if 'TRAVIS' in os.environ:
    DOCKIT_BACKENDS['mongo'] = {'ENGINE':'dockit.backends.mongo.backend.MongoDocumentStorage',
                                'USER':'travis',
                                'PASSWORD':'test',
                                'DB':'mydb_test',
                                'HOST':'127.0.0.1',
                                'PORT':27017,}
    DOCKIT_INDEX_BACKENDS['mongo'] = {'ENGINE':'dockit.backends.mongo.backend.MongoIndexStorage',
                                'USER':'travis',
                                'PASSWORD':'test',
                                'DB':'mydb_test',
                                'HOST':'127.0.0.1',
                                'PORT':27017,}
    if 'dockit.backends.mongo' not in INSTALLED_APPS:
        INSTALLED_APPS.append('dockit.backends.mongo')

if os.environ.get('TASK_BACKEND', None) == 'celery':
    DOCKIT_INDEX_BACKENDS['djangodocument']['INDEX_TASKS'] = 'dockit.backends.djangodocument.tasks.CeleryIndexTasks'
    INSTALLED_APPS += ["djcelery"]
    CELERY_ALWAYS_EAGER = True
    
    import djcelery
    djcelery.setup_loader()
if os.environ.get('TASK_BACKEND', None) == 'ztask':
    DOCKIT_INDEX_BACKENDS['djangodocument']['INDEX_TASKS'] = 'dockit.backends.djangodocument.tasks.ZTaskIndexTasks'
    INSTALLED_APPS += ["django_ztask"]
    ZTASKD_ALWAYS_EAGER = True

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
