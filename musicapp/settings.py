"""
Django settings for musicapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f_#2#8x@j@b^1%3h(6kk_hzn#myylx3a45qt&5zu1e&pmvzjtk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # elasticsearch'e index atarken kullaniyorum
    'requests',

    'setlist',
    'rest_framework',
    'api',

    'rest_framework.authtoken',
    'corsheaders',

    'social.apps.django_app.default',
    'tldextract',

    #bu 3 tanesi alakali - pytz time zone
    'actstream',
    'jsonfield',
    'pytz',

)



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)


SOCIAL_AUTH_PIPELINE = (
     'social.pipeline.social_auth.social_details',
     'social.pipeline.social_auth.social_uid',
     'social.pipeline.social_auth.auth_allowed',
     'social.pipeline.social_auth.social_user',
     'social.pipeline.user.get_username',
     'social.pipeline.social_auth.associate_by_email',
     'social.pipeline.user.create_user',
     'social.pipeline.social_auth.associate_user',
     'social.pipeline.social_auth.load_extra_data',
     'social.pipeline.user.user_details',
     'api.pipeline.save_profile_picture',
 )


ROOT_URLCONF = 'musicapp.urls'

WSGI_APPLICATION = 'musicapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR +'/static/'

LOGIN_URL = '/entry/'
MEDIA_ROOT = BASE_DIR +'/media/'
MEDIA_URL = '/media/'
AUTH_USER_MODEL = 'setlist.User'


# Daha sonra bunun icin bir whitelist gelistirebiliriz..
CORS_ORIGIN_ALLOW_ALL = True
#bundan cok emin degilim
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.ExpiringTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
    ),
    # Use Django's standard `django.contrib.auth` permissions,
     # or allow read-only access for unauthenticated users.
     'DEFAULT_PERMISSION_CLASSES': [
         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
     ],
}

SOCIAL_AUTH_FACEBOOK_KEY = '1426533514262555'
SOCIAL_AUTH_FACEBOOK_SECRET = '8c0354c414335f8a7d748f45ea97d5f8'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

AUTHENTICATION_BACKENDS = (
      'social.backends.facebook.FacebookOAuth2',
      'django.contrib.auth.backends.ModelBackend',
  )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',

)

ACTSTREAM_SETTINGS = {
    'MANAGER': 'actstream.managers.ActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}