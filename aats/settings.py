"""
Django settings for ttas project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os, logging
import django.utils.log
import logging.handlers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r@_o-q0fw)_&k#i2)6jd9-qjvvj^0tvi6%*2!8ny1#mo)wlyo-'

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'celery',
    'djcelery',
    'product',
    'Users',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aats.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'aats.wsgi.application'
AUTH_USER_MODEL = 'Users.User'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
ENV_PROFILE = os.getenv("ENV")

if ENV_PROFILE == "env":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'TT',
            'USER': 'root',
            'PASSWORD': '123456',
            'HOST': '127.0.0.1',
            # 数据库的端口号
            'PORT': '3306'
        },
    }
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PICKLE_VERSION": -1
            }
        }
    }
    DEBUG = True
    BROKERURL = 'redis://127.0.0.1:6379/15'
    CELERYRESULTBACKEND = 'redis://127.0.0.1:6379/14'

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'TT',
            'USER': 'root',
            'PASSWORD': 'yuan@KXM1023',
            'HOST': '47.98.224.226',
            # 数据库的端口号
            'PORT': '3306'
        },
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://47.98.224.226/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PICKLE_VERSION": -1
            }
        }
    }
    DEBUG = False
    BROKERURL = 'redis://47.98.224.226:6379/15'
    CELERYRESULTBACKEND = 'redis://47.98.224.226:6379/14'

# # 连接mangodb
# import mongoengine
#
# # 连接mongodb中数据库名称为mongotest5的数据库
# conn = mongoengine.connect("TT")


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'utils.auth.JSONWebTokenAuthentication'
    ),
    'DEFAULT_PAGINATION_CLASS': 'Users.custompage.CustomPagination',
    'PAGE_SIZE': 10,  # 每页数目
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

    # 异常返回
    'EXCEPTION_HANDLER': (
        'utils.custom_exception.custom_exception_handler'
    )
}

import datetime

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'Users.utils.jwt_response_payload_handler',  # 后面跟着你视图里定义函数
    'JWT_RESPONSE_PAYLOAD_ERROR_HANDLER': 'utils.jwt_response.jwt_response_payload_error_handler',
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {  # 格式化
#         'simple': {
#             'format': '[%(asctime)s %(levelname)s] %(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S'
#         },
#         'console': {
#             'format': '[%(asctime)s][%(levelname)s]  %(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S'
#         }
#     },
#     'handlers': {  # 处理器
#         'console': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#             'formatter': 'console'
#         },
#         'fileHandler': {
#             'level': 'INFO',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'formatter': 'simple',
#             'filename': 'art.log'
#         }
#
#     },
#     'loggers': {  # 记录器
#         'mdjango': {
#             'handlers': ['console', 'fileHandler'],
#             'level': 'INFO',
#             'propagate': False
#         }
#
#     }
# }

CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = TIME_ZONE
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# # # CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# #
# CELERYD_MAX_TASKS_PER_CHILD = 100 # 每个worker最大执行数，长时间执行造成内存泄露/
# CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# from djcelery.schedulers import DatabaseScheduler
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # 定时任务调度器


# 图片设置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
