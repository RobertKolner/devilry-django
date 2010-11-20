# Django settings for devilry project.
from os.path import abspath, dirname, join

this_dir = dirname(abspath(__file__))


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# If no admins are set, no emails are sent to admins
ADMINS = (
     ('Devilry admin', 'admin@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': join(this_dir, 'db.sqlite3'),    # Or path to database file if using sqlite3.
        'USER': '',             # Not used with sqlite3.
        'PASSWORD': '',         # Not used with sqlite3.
        'HOST': '',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',             # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = join(this_dir, "filestore")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+g$%**q(w78xqa_2)(_+%v8d)he-b_^@d*pqhq!#2p*a7*9e9h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'devilry.core.utils.profile.ProfilerMiddleware'
]


ROOT_URLCONF = 'devilry.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(this_dir, 'templates'),
)


LOGIN_URL = '/ui/login'
DEVILRY_LOGOUT_URL = '/ui/logout'


#DEVILRY_APPS = [
    #'devilry.core',
    #'devilry.ui',
    #'devilry.adminscripts',
    #'devilry.addons.student',
    #'devilry.addons.examiner',
    #'devilry.addons.admin',
    #'devilry.addons.aboutme',
    #'devilry.addons.grade_approved',
    #'devilry.addons.grade_default',
    #'devilry.addons.grade_rstschema',
    #'devilry.addons.gradestats',
    #'devilry.addons.xmlrpc_examiner',
    #'devilry.addons.quickdash',
    #'devilry.xmlrpc',
    #'devilry.xmlrpc_client'
#]

#INSTALLED_APPS = [
    #'django.contrib.webdesign', 
    #'django.contrib.markup', 
    #'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.admin',
    #'django.contrib.auth',
    #'django.contrib.contenttypes'
#] + DEVILRY_APPS


INSTALLED_APPS = (
    'django.contrib.markup', 
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'devilry.addons.student',
    'devilry.addons.examiner',
    'devilry.addons.admin',
    'devilry.addons.grade_approved',
    'devilry.addons.grade_default',
    'devilry.addons.grade_schema',
    'devilry.addons.grade_rstschema',
    'devilry.addons.quickdash',
    'devilry.addons.xmlrpc_examiner',
    'devilry.xmlrpc',
    'devilry.xmlrpc_client',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'devilry.core',
    'devilry.ui',
    'devilry.adminscripts',
    'devilry.addons.gradestats',
    'devilry.rst'
)




DEVILRY_RESOURCES_ROOT = join(this_dir, 'resources')
DEVILRY_RESOURCES_URL = '/resources'
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth", 
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'devilry.core.templatecontext.template_variables',
)



DELIVERY_STORE_BACKEND = 'devilry.core.deliverystore.FsDeliveryStore'
DELIVERY_STORE_ROOT = join(this_dir, 'deliverystore')
#DELIVERY_STORE_BACKEND = 'devilry.core.deliverystore.DbmDeliveryStore'
#DELIVERY_STORE_DBM_FILENAME = join(this_dir, 'deliverystore', 'deliverystore.dbm')

# Make sure this does not end with / (i.e. '' means / is the main page).
DEVILRY_MAIN_PAGE = ''

# The base template used by devilry. Override for simple theming
BASE_TEMPLATE = 'devilry/base.django.html'

MEDIA_ICONS_URL = 'media/icons/'
#JQUERY_UI_THEME = 'devilry'
#JQUERY_UI_THEME = 'dot-luv'
#JQUERY_UI_THEME = 'ui-darkness'
JQUERY_UI_THEME = 'devilry-blue'

SEND_EMAIL_TO_USERS = False

## The default grade-plugin
DEVILRY_DEFAULT_GRADEPLUGIN='grade_default:charfieldgrade'
#DEVILRY_DEFAULT_GRADEPLUGIN='grade_default:approvedgrade'
#DEVILRY_DEFAULT_GRADEPLUGIN='grade_rstschema:rstschemagrade'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = this_dir + '/email_log/'

EMAIL_SUBJECT_PREFIX = '[devilry] '
EMAIL_SUBJECT_PREFIX_ADMIN = '[devilry-admin] '

WEB_PAGE_PREFIX = 'http://devilry.ifi.uio.no/django/main'
EMAIL_DEFAULT_FROM = 'devilry-support@ifi.uio.no'
EMAIL_SIGNATURE = "This is a message from the Devilry assignment delivery system. " \
                  "Please do not respond to this email."

DEVILRY_SYSTEM_ADMIN_EMAIL='devilry-support@example.com'

DATETIME_FORMAT = "N j, Y, H:i"

#Set max file size to 5MB. Files greater than this size are split into chunks of this size.
MAX_ARCHIVE_CHUNK_SIZE = 5000000
