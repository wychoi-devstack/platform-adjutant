# Copyright (C) 2015 Catalyst IT Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Django settings for user_reg project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+er!!4olta#17a=n%uotcazg2ncpl==yjog%1*o-(cr%zys-)!'

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
    'rest_framework',
    'base',
    'api_v1',
    'tenant_setup',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user_reg.middleware.KeystoneHeaderUnwrapper',
    'user_reg.middleware.RequestLoggingMiddleware'
)

if 'test' in sys.argv:
    # modify MIDDLEWARE_CLASSES
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.remove('user_reg.middleware.KeystoneHeaderUnwrapper')
    MIDDLEWARE_CLASSES.append('user_reg.middleware.TestingHeaderUnwrapper')

ROOT_URLCONF = 'user_reg.urls'

WSGI_APPLICATION = 'user_reg.wsgi.application'


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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'reg_log.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'keystonemiddleware': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# App apecific settings:

USERNAME_IS_EMAIL = True

# Keystone admin credentials:
KEYSTONE = {
    'username': 'admin',
    'password': 'openstack',
    'project_name': 'admin',
    'auth_url': "http://localhost:5000/v2.0"
}

DEFAULT_REGION = "REGION_ONE"

NETWORK_DEFAULTS = {
    "REGION_ONE": {
        'network_name': 'somenetwork',
        'subnet_name': 'somesubnet',
        'router_name': 'somerouter',
        # this depends on region and needs to be pulled from somewhere:
        'public_network': 'aed4df5a-1a1f-42e4-b105-aa7f2edc7a95',
        'DNS_NAMESERVERS': ['193.168.1.2',
                            '193.168.1.3'],
        'SUBNET_CIDR': '192.168.1.0/24'
    }
}

# the order of the actions matters. These will run after the default action,
# in the given order.
API_ACTIONS = {'CreateProject': ['AddAdminToProject',
                                 'DefaultProjectResources']}

# This is populated from the various model modules at startup:
ACTION_CLASSES = {}
