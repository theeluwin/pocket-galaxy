import os

from os import getenv
from os.path import abspath
from os.path import join as pjoin
from os.path import dirname as dname
from datetime import timedelta


# basic
PROJECT_SLUG = 'project'
BASE_DIR = dname(dname(abspath(__file__)))
SHARED_DIR = '/shared'

# credential
SECRET_KEY = getenv('SECRET_KEY', "It's a secret to everybody!")
try:
    DEBUG = bool(int(os.getenv('DEBUG', False)))
except ValueError:
    DEBUG = False
if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [host for host in getenv('ALLOWED_HOSTS', '').split(',') if host]
CORS_ORIGIN_ALLOW_ALL = True  # hurry up! we don't have time..

# app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_filters',
    'rest_framework',
    'app',
]
ROOT_URLCONF = f'{PROJECT_SLUG}.urls'
WSGI_APPLICATION = f'{PROJECT_SLUG}.wsgi.application'

# middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
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

# i18n
LANGUAGE_CODE = 'ko'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# static & media
STATIC_URL = '/static/'
STATIC_ROOT = pjoin(SHARED_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = pjoin(SHARED_DIR, 'mediafiles')

# template
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': pjoin(SHARED_DIR, 'dbfiles', 'db.sqlite3'),
    }
}

# rest
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'project.paginations.GeneralPageNumberPagination',
}

# jwt
JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': 'user_session',
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': timedelta(minutes=10),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=90),
    'JWT_LEEWAY': 3600 * 24 * 7,
}

# custom
ADMIN_TITLE = 'Pocket Galaxy Admin'
