"""
Django settings for webprice project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k59g*za)_)q*z+8c#mwk^mpentj3v9te=5ws@4k))ht(_$i#_='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1','localhost','.now.sh']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'tailwind',
    'theme',
    'django_icons',
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'webprice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dashboard.global_function.notifications',
                'dashboard.global_function.sidebar_menus',
            ],
        },
    },
]

WSGI_APPLICATION = 'webprice.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PGNAME'),
        'USER': os.getenv('PGUSER'),
        'PASSWORD': os.getenv('PGPASS'),
        'HOST': os.getenv('PGHOST'),
        'PORT': os.getenv('PGPORT'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, STATIC_URL)]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', STATIC_URL)

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']


DJANGO_ICONS = {
    "ICONS": {
        "dashboard": {"name": "fa-solid fa-house"},
        "add-product": {"name": "fa-solid fa-square-plus"},
        "view-products": {"name": "fa-solid fa-eye"},
        "profile": {"name": "fa-solid fa-user"},
        "settings": {"name": "fa-solid fa-gear"},
        "lastPage": {"name": "fa-solid fa-angles-right"},
        'delete': {"name": "fa-solid fa-trash"},
        "edit": {"name": "fa-solid fa-pen"},
        "group": {"name": "fa-solid fa-cart-shopping"},
        "user": {"name": "fa-solid fa-user"},
        "google": {"name": "fa-brands fa-google"},
        "bell": {"name": "fa-solid fa-bell"},
        "notifications": {"name": "fa-solid fa-bell"},
        "search": {"name": "fa-solid fa-magnifying-glass"},
        "eye": {"name": "fa-solid fa-eye"},
        "eye-slash": {"name": "fa-solid fa-eye-slash"},
        "logout": {"name": "fa-solid fa-right-from-bracket"},
        "up": {"name": "fa-solid fa-caret-up"},
        "down": {"name": "fa-solid fa-caret-down"},
        "cross": {"name": "fa-solid fa-xmark"},
        "check": {"name": "fa-solid fa-check"}
    },
}

# Redirect URLs after login/logout
LOGIN_REDIRECT_URL = 'dashboard'  # Redirect to your desired view after login
LOGOUT_REDIRECT_URL = 'account_login'  # Redirect to login view after logout



MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
    }

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_USE_TLS = True  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_HOST_USER = os.getenv('EMAIL_USER') 
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS') 
EMAIL_PORT = 587  

# django_project/settings.py
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1  # new

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

TIME_ZONE = 'Asia/Kathmandu'

