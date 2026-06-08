"""
Django settings for faidChatbot project.
Optimized for Production Deployment.
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-h_q3wl7=flr(2pf&&x)qn(4#q69)yx3@gwf&ltag33p8ig9fp0')

# SECURITY WARNING: don't run with debug turned on in production!
# Toggles automatically if an environment flag named RENDER is present
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'laborious-brande-relievedly.ngrok-free.dev',
    'faidchatbot.onrender.com',
    '.vercel.app',
]

# Render automatically creates a unique host address variable name for your web dashboard service
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # WhiteNoise requires positioning right before the staticfiles engine app
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'profiles.apps.ProfilesConfig',
    'authentication',
    'chat',
    'history',
    'homepage',
    'ussd',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WHITENOISE MIDDLEWARE: Must sit exactly here right below SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'faidChatbot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "profiles.context_processor.user_profile",
            ],
        },
    },
]

WSGI_APPLICATION = 'faidChatbot.wsgi.application'

# Database Setup configuration
# Safely falls back to local sqlite3 file if DATABASE_URL environment token is absent
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require='RENDER' in os.environ
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'authentication.validators.StrongPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage optimization engine for production static tracking
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GEMINI_API_KEY = config('GEMINI_API_KEY')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1
SOCIALACCOUNT_STORE_TOKENS = False

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID', default=''),
            'secret': config('GOOGLE_SECRET_KEY', default=''),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
