# -*- coding: utf-8 -*-

"""
Data Entry System v2
Copyright (C) 2019-2023  Javier Garcia Gonzalez javiergargon@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=p^0qq+f98+0$ers0u(!vym9f+bt#wa-ii#^2vdqpc0yx#bm*g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('de', 'German'),
    ('fr', 'French'),
)

PARLER_LANGUAGES = {
    None: (
        {'code': 'en',}, # English
        {'code': 'fr',}, # French
        {'code': 'es',}, # Spanish
        {'code': 'de',}, # German
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
#    'django.contrib.staticfiles',
    "parler",
    "main",
    "docs",
    "entry",
    "campaigns"
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

ROOT_URLCONF = 'DataEntry_v2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'DataEntry_v2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dataEntry2',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'DEUser',
        'PASSWORD': 'CqjiUH8JhaArZS7a',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',
        'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'; " # Set to empty string for default.
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = ( os.path.join(BASE_DIR, 'locale'), )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/st/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, "st")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# CELERY STUFF
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'

TESSERACT_LANGS = (
    ('afr', 'afr'),
    ('all', 'all'),
    ('amh', 'amh'),
    ('ara', 'ara'),
    ('asm', 'asm'),
    ('aze', 'aze'),
    ('aze-cyrl', 'aze-cyrl'),
    ('bel', 'bel'),
    ('ben', 'ben'),
    ('bod', 'bod'),
    ('bos', 'bos'),
    ('bre', 'bre'),
    ('bul', 'bul'),
    ('cat', 'cat'),
    ('ceb', 'ceb'),
    ('ces', 'ces'),
    ('chi-sim', 'chi-sim'),
    ('chi-sim-vert', 'chi-sim-vert'),
    ('chi-tra', 'chi-tra'),
    ('chi-tra-vert', 'chi-tra-vert'),
    ('chr', 'chr'),
    ('cos', 'cos'),
    ('cym', 'cym'),
    ('dan', 'dan'),
    ('deu', 'deu'),
    ('div', 'div'),
    ('dzo', 'dzo'),
    ('ell', 'ell'),
    ('eng', 'eng'),
    ('enm', 'enm'),
    ('epo', 'epo'),
    ('est', 'est'),
    ('eus', 'eus'),
    ('fao', 'fao'),
    ('fas', 'fas'),
    ('fil', 'fil'),
    ('fin', 'fin'),
    ('fra', 'fra'),
    ('frk', 'frk'),
    ('frm', 'frm'),
    ('fry', 'fry'),
    ('gla', 'gla'),
    ('gle', 'gle'),
    ('glg', 'glg'),
    ('grc', 'grc'),
    ('guj', 'guj'),
    ('hat', 'hat'),
    ('heb', 'heb'),
    ('hin', 'hin'),
    ('hrv', 'hrv'),
    ('hun', 'hun'),
    ('hye', 'hye'),
    ('iku', 'iku'),
    ('ind', 'ind'),
    ('isl', 'isl'),
    ('ita', 'ita'),
    ('ita-old', 'ita-old'),
    ('jav', 'jav'),
    ('jpn', 'jpn'),
    ('jpn-vert', 'jpn-vert'),
    ('kan', 'kan'),
    ('kat', 'kat'),
    ('kat-old', 'kat-old'),
    ('kaz', 'kaz'),
    ('khm', 'khm'),
    ('kir', 'kir'),
    ('kmr', 'kmr'),
    ('kor', 'kor'),
    ('kor-vert', 'kor-vert'),
    ('lao', 'lao'),
    ('lat', 'lat'),
    ('lav', 'lav'),
    ('lit', 'lit'),
    ('ltz', 'ltz'),
    ('mal', 'mal'),
    ('mar', 'mar'),
    ('mkd', 'mkd'),
    ('mlt', 'mlt'),
    ('mon', 'mon'),
    ('mri', 'mri'),
    ('msa', 'msa'),
    ('mya', 'mya'),
    ('nep', 'nep'),
    ('nld', 'nld'),
    ('nor', 'nor'),
    ('oci', 'oci'),
    ('ori', 'ori'),
    ('osd', 'osd'),
    ('pan', 'pan'),
    ('pol', 'pol'),
    ('por', 'por'),
    ('pus', 'pus'),
    ('que', 'que'),
    ('ron', 'ron'),
    ('rus', 'rus'),
    ('san', 'san'),
    ('sin', 'sin'),
    ('slk', 'slk'),
    ('slv', 'slv'),
    ('snd', 'snd'),
    ('spa', 'spa'),
    ('spa-old', 'spa-old'),
    ('sqi', 'sqi'),
    ('srp', 'srp'),
    ('srp-latn', 'srp-latn'),
    ('sun', 'sun'),
    ('swa', 'swa'),
    ('swe', 'swe'),
    ('syr', 'syr'),
    ('tam', 'tam'),
    ('tat', 'tat'),
    ('tel', 'tel'),
    ('tgk', 'tgk'),
    ('tha', 'tha'),
    ('tir', 'tir'),
    ('ton', 'ton'),
    ('tur', 'tur'),
    ('uig', 'uig'),
    ('ukr', 'ukr'),
    ('urd', 'urd'),
    ('uzb', 'uzb'),
    ('uzb-cyrl', 'uzb-cyrl'),
    ('vie', 'vie'),
    ('yid', 'yid'),
    ('yor', 'yor')
 )
