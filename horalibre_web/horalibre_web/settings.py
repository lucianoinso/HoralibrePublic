"""
Django settings for horalibre_web project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from django.conf.global_settings import DATETIME_INPUT_FORMATS, DATE_INPUT_FORMATS
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PYTHONIOENCODING="UTF-8"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'YOURSECRETKEYGOESHERE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'administration.apps.AdministrationConfig',
    'commentary.apps.CommentaryConfig',
    'login.apps.LoginConfig',
    'news.apps.NewsConfig',
    'records.apps.RecordsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'horalibre_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'horalibre_web', 'templates'),
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'horalibre_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbname',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGS_DIR = os.path.join(BASE_DIR, "logs")

# EMAIL STUFF
EMAIL_USE_TLS = True
EMAIL_HOST = 'yoursmtpserver'
EMAIL_HOST_USER = 'youremail@company.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
EMAIL_PORT = 587

# DATE_INPUT_FORMATS += (
#     '%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y', # '2006-10-25', '10/25/2006', '10/25/06'
#     '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
#     '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
# )

# DATETIME_INPUT_FORMATS += (
#     '%d-%m-%Y %H:%M:%S',     # '2006-10-25 14:30:59'
#     '%d-%m-%Y %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
#     '%d-%m-%Y %H:%M',        # '2006-10-25 14:30'
#     '%d-%m-%Y',              # '2006-10-25'
#     '%d/%m/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
#     '%d/%m/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
#     '%d/%m/%Y %H:%M',        # '10/25/2006 14:30'
#     '%d/%m/%Y',              # '10/25/2006'
#     '%d/%m/%y %H:%M:%S',     # '10/25/06 14:30:59'
#     '%d/%m/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
#     '%d/%m/%y %H:%M',        # '10/25/06 14:30'
#     '%d/%m/%y',              # '10/25/06']
# )

