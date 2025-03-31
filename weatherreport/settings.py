# You should not edit this file
from django.contrib import messages
from pathlib import Path
import tempfile
import os

VISUAL_CROSSING_API_KEY = os.environ.get('VISUAL_CROSSING_API_KEY', 'TQL3933V6UQB8GFCCUTGBYL4K')

BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings for development; update for production as needed.
DEBUG = True
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ALLOW_ALL_ORIGINS = True

SECRET_KEY = 'django-insecure-session-key'

# For our React SPA, we explicitly allow unauthenticated users.
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'data_wizard',
    'data_wizard.sources',
    'crispy_forms',
    'crispy_bootstrap5',
    'weather',       
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

# Update the root URL configuration to use your project module.
ROOT_URLCONF = 'weatherreport.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add custom template directories here if needed.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

# WSGI application configuration.
WSGI_APPLICATION = 'weatherreport.wsgi.application'

# Database for development (SQLite).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalisation settings.
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [('en', 'English')]

# Locale path updated for the weather app.
LOCALE_PATHS = [BASE_DIR / 'weather' / 'locale']

# Static files settings.
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'

# Media files settings.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Optional: Configuration for crispy forms if used.
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Account redirect URLs.
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'


CORS_ALLOW_ALL_ORIGINS = True

# Email Backend: saves emails to a temporary directory for development.
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
DEFAULT_FROM_EMAIL = 'hp00803@surrey.ac.uk'
EMAIL_FILE_PATH = tempfile.mkdtemp()

