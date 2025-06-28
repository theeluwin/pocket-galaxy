from os import getenv
from pathlib import Path
from datetime import timedelta


# custom
ADMIN_TITLE = 'Pocket Galaxy Admin'

# path
BASE_DIR = Path(__file__).resolve().parent.parent
SHARED_ROOT = Path('/shared')

# credential
SECRET_KEY = getenv('SECRET_KEY', "It's a secret to everybody!")
try:
    DEBUG = bool(int(getenv('DEBUG', False)))
except ValueError:
    DEBUG = False
HOST = getenv('HOST', 'localhost')

# security
SECURE_PROXY_SSL_HEADER = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'corsheaders',
    'app',
]

# wsgi
WSGI_APPLICATION = 'project.wsgi.application'

# url
APPEND_SLASH = True
ROOT_URLCONF = 'project.urls'

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

# password
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

# resource
STATIC_URL = '/static/'
STATIC_ROOT = SHARED_ROOT / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = SHARED_ROOT / 'mediafiles'

# log
LOG_ROOT = SHARED_ROOT / 'logfiles'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '<%(asctime)s> %(levelname)s %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT / 'django.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'standard',
        },
        'request': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT / 'django.request.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'standard',
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT / 'django.sql.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'standard',
        },
        'project': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_ROOT / 'django.project.log',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['sql'] if DEBUG else [],
            'level': 'DEBUG',
            'propagate': False,
        },
        'project': {
            'handlers': ['console', 'project'] if DEBUG else ['project'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

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
        'NAME': SHARED_ROOT / 'dbfiles' / 'db.sqlite3',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# rest
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'project.paginations.GeneralPageNumberPagination',
}

# jwt
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_COOKIE': 'user_session',
    'AUTH_COOKIE_DOMAIN': None,
    'AUTH_COOKIE_SECURE': not DEBUG,
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE': 'Lax',
    'LEEWAY': 3600 * 24 * 7,
}

# host
ALLOWED_HOSTS = [HOST]
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    f'http://{HOST}',
    f'https://{HOST}',
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CSRF_TRUSTED_ORIGINS = [
    f'http://{HOST}',
    f'https://{HOST}',
]
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
