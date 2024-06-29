"""
Django settings for inmuebles project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
#from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
#env_path = BASE_DIR / '.env'
#load_dotenv(dotenv_path=env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY') or ImproperlyConfigured("SECRET_KEY not set")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    'hlata-dev.cl',
    'www.hlata-dev.cl',
    'apps.hlata-dev.cl',
    'inmuebles-kristen.apps.hlata-dev.cl',
    'inmuebleskristen.shop',
    'www.inmuebleskristen.shop'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'corsheaders',
    'sslserver',
    'anymail',
    'web'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'inmuebles.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'inmuebles.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

name = os.environ.get('BDD_NAME') or ImproperlyConfigured("BDD_NAME not set")
user = os.environ.get('BDD_USER') or ImproperlyConfigured("BDD_USER not set")
password = os.environ.get('BDD_PASSWORD') or ImproperlyConfigured("BDD_PASSWORD not set")
host = os.environ.get('BDD_HOST') or ImproperlyConfigured("BDD_HOST not set")
port = os.environ.get('BDD_PORT') or ImproperlyConfigured("BDD_PORT not set")

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
        'OPTIONS': {
            'client_encoding': 'UTF8',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'web.Usuario'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_WHITELIST = [
'http://localhost:8000',
'http://127.0.0.1:8000',
'http://inmuebleskristen.shop',
'https://inmuebleskristen.shop',
'http://www.inmuebleskristen.shop',
'https://www.inmuebleskristen.shop',
'http://apps.hlata-dev.cl',
'https://apps.hlata-dev.cl',
'http://inmuebles-kristen.apps.hlata-dev.cl',
'https://inmuebles-kristen.apps.hlata-dev.cl',
'http://inmuebles-kristen-db.apps.hlata-dev.cl',
'https://inmuebles-kristen-db.apps.hlata-dev.cl',
]

##### Site Settings

SITE_ID = 1

##### Email Settings


## CONSOLE
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# SLACK_API_KEY = os.environ.get('SLACK_API_KEY')
# ZOHO
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND') or ImproperlyConfigured("EMAIL_BACKEND not set")
EMAIL_HOST = os.environ.get('EMAIL_HOST') or ImproperlyConfigured("EMAIL_HOST not set")
EMAIL_PORT = os.environ.get('EMAIL_PORT') or ImproperlyConfigured("EMAIL_PORT not set")
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') or ImproperlyConfigured("EMAIL_USE_TLS not set")
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') or ImproperlyConfigured("EMAIL_HOST_USER not set")
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') or ImproperlyConfigured("EMAIL_HOST_PASSWORD not set")
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL') or ImproperlyConfigured("DEFAULT_FROM_EMAIL not set")
DEFAULT_CONTACT_NOTICE_EMAIL = os.environ.get('DEFAULT_CONTACT_NOTICE_EMAIL') or ImproperlyConfigured("DEFAULT_CONTACT_NOTICE_EMAIL not set")

# ANYMAIL
# DEFAULT_CONTACT_NOTICE_EMAIL = os.environ.get('DEFAULT_CONTACT_NOTICE_EMAIL')
# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
# ANYMAIL = {
#     "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY'),
#     "MAILGUN_SENDER_DOMAIN": os.environ.get('MAILGUN_SENDER_DOMAIN'),
#     "MAILGUN_API_URL" : "https://api.mailgun.net/v3/",
#     "MAILGUN_API_SENDER": os.environ.get('MAILGUN_API_SENDER'),
#     "MAILGUN_SEND_DEFAULTS": {
#         "html": True,
#         "inline_css": True,  # Enable inline CSS in HTML emails
#     },
# }
# EMAIL_USE_TLS = True

