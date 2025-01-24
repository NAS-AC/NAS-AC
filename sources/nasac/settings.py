from datetime import timedelta
from pathlib import Path

from django.template.defaultfilters import upper

import os
import yaml

import logging

logger = logging.getLogger(__name__)

CONFIG_FILE = '/data/properties.yaml'
configs = {}
def set_configs(prefix, data):
	for key, value in data.items():
		if isinstance(value, dict):
			set_configs(f"{prefix}{key}_", value)
		else:
			configs[upper("{prefix}{key}")] = value
if not os.path.exists(CONFIG_FILE):
	CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../resources/properties.yaml')
try:
	with open(CONFIG_FILE, "r") as f:
		config = yaml.safe_load(f)
	set_configs("", config)
except FileNotFoundError:
	raise FileNotFoundError(f"Configuration file '{CONFIG_FILE}' not found.")
except yaml.YAMLError as e:
	raise RuntimeError(f"Error reading YAML file: {e}")

logger.info(configs)
# logger.info(configs.DEBUG)
# logger.info(configs.AUTHENTICATION_APP)
# logger.info(configs.AUTHENTICATION_TEST)

#-----------------------
#Not changeable settings
#-----------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = '/data/files'
MEDIA_URL = '/files/'
ROOT_URLCONF = 'nasac.urls'
WSGI_APPLICATION = 'nasac.wsgi.application'
STATIC_URL = 'static/'


#TODO: -----------------------------------------------
#TODO: No clue what this is, should i make it modular?
#TODO: -----------------------------------------------
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
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
	'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
	'ROTATE_REFRESH_TOKENS': True,
	'BLACKLIST_AFTER_ROTATION': True,
}
REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
	),
	'DEFAULT_RENDERER_CLASSES': [
		'rest_framework.renderers.JSONRenderer',
	],
}

#TODO: -------------------------------------------------
#TODO: This needs to be modular, but I dont know how yet
#TODO: -------------------------------------------------
LOGGING = {
	'version': 1,
	'handlers': {
		'console': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console'],
			'level': 'DEBUG',
			'propagate': True,
		},
		'core': {
			'handlers': ['console'],
			'level': 'DEBUG',
			'propagate': False,
		},
	},
}
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': '/data/db.sqlite3',
	}
}
USE_I18N = True
USE_TZ = True

#-------------------------------------
#Settings with not changeable defaults
#-------------------------------------
INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'core',

	'rest_framework',
	'drf_yasg',
]
for app in configs.APPS if 'APPS' in configs.keys() else []:
	INSTALLED_APPS.append(app)
MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
]
for middleware in configs.MIDDLEWARE if 'MIDDLEWARE' in configs.keys() else []:
	MIDDLEWARE.append(middleware)

#-------------------------------------
#Mandatory Settings
#-------------------------------------
SECRET_KEY = configs.SECRET_KEY if 'SECRET_KEY' in configs.keys() else 'django-insecure-6rff$ukcwd(3#c52qb6d5+3%1+lcet_npbo-eo$2)-!uvq@vg9'

#-------------------------------------
#Optional Settings
#-------------------------------------
DEBUG = configs.DEBUG if 'DEBUG' in configs.keys() else 'False'
ALLOWED_HOSTS = configs.ALLOWED_HOSTS if 'ALLOWED_HOSTS' in configs.keys() else ['*']
LANGUAGE_CODE = configs.LANGUAGE_CODE if 'LANGUAGE_CODE' in configs.keys() else 'en-us'
TIME_ZONE = configs.TIME_ZONE if 'TIME_ZONE' in configs.keys() else 'UTC'
AUTHENTICATION_APP = configs.AUTHENTICATION_APP if 'AUTHENTICATION_APP' in configs.keys() else 'core'

#TODO: this 2 are not implemented
AUTHENTICATION_CLASS = configs.AUTHENTICATION_CLASS if 'AUTHENTICATION_CLASS' in configs.keys() else 'rest_framework.authentication.TokenAuthentication'
AUTHENTICATION_PERMISSION_CLASSES = configs.AUTHENTICATION_PERMISSION_CLASSES if 'AUTHENTICATION_PERMISSION_CLASSES' in configs.keys() else ['rest_framework.authentication.TokenAuthentication']

