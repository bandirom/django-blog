import os
from pathlib import Path

from .additional_settings import *

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-b2sh!qk&=%azim-=s&=d1(-1upbq7H&-^-=tmPeHPLKXD')

DEBUG = int(os.environ.get('DEBUG', 1))

ALLOWED_HOSTS: list = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

if DEBUG:
    ALLOWED_HOSTS: list = ['*']

AUTH_USER_MODEL = 'main.User'

PROJECT_TITLE = os.environ.get('PROJECT_TITLE', 'Template')

GITHUB_URL = os.environ.get('GITHUB_URL', 'https://github.com')

REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379')

USE_HTTPS = int(os.environ.get('USE_HTTPS', 0))
ENABLE_SENTRY = int(os.environ.get('ENABLE_SENTRY', 0))
ENABLE_SILK = int(os.environ.get('ENABLE_SILK', 0))
ENABLE_DEBUG_TOOLBAR = int(os.environ.get('ENABLE_DEBUG_TOOLBAR', 0))

INTERNAL_IPS: list[str] = []

ADMIN_URL = os.environ.get('ADMIN_URL', 'admin')

SWAGGER_URL = os.environ.get('SWAGGER_URL')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:8008')
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8008')

HEALTH_CHECK_URL = os.environ.get('HEALTH_CHECK_URL', '/application/health/')

CHAT_API_URL = os.environ.get('CHAT_API_URL')
CHAT_API_KEY = os.environ.get('CHAT_API_KEY')
CHAT_PROXY = os.environ.get('CHAT_PROXY')

USER_AVATAR_MAX_SIZE = 4.0
USER_FILE_MAX_SIZE = 10.0  # Mb
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # b = 10 MB

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
EMAIL_CONFIRMATION_EXPIRE_SECONDS = 3 * 60 * 60 * 24

API_KEY_HEADER = os.environ.get('API_KEY_HEADER')
API_KEY = os.environ.get('API_KEY')

GRAPHENE = {'SCHEMA': 'main.schema.schema'}


GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:8000/auth/google')

SOCIAL_ACCOUNTS_PROVIDERS = {
    'google': {
        'enabled': True,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'SCOPE': [
            'email',
            'profile',
            'openid',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'OAUTH_PKCE_METHOD': 'S256',
    }
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'rosetta',
    'django_summernote',
    'django_filters',
    'graphene_django',
]

LOCAL_APPS = [
    'main.apps.MainConfig',
    'auth_app.apps.AuthAppConfig',
    'blog.apps.BlogConfig',
    'contact_us.apps.ContactUsConfig',
    'user_profile.apps.UserProfileConfig',
    'actions.apps.ActionsConfig',
]

INSTALLED_APPS += THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'main.middleware.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('main.auth_backend.JWTCookieAuthentication',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'main.pagination.BasePageNumberPagination',
}


ROOT_URLCONF = 'src.urls'

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'src.wsgi.application'
ASGI_APPLICATION = 'src.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('POSTGRES_DB', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'CONN_MAX_AGE': 0,
    },
}

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TZ', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

LANGUAGES = (('en', 'English'),)

SESSION_COOKIE_NAME = 'sessionid_blog'
CSRF_COOKIE_NAME = 'csrftoken_blog'

ROSETTA_SHOW_AT_ADMIN_PANEL = DEBUG
REST_AUTH_TOKEN_MODEL = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': 'INFO', 'handlers': ['default']},
    'formatters': {
        'simple': {'format': '%(levelname)s %(message)s'},
        'verbose': {'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'},
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {'level': 'INFO', 'propagate': True},
        'django.request': {
            'handlers': ['django.server'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

SPECTACULAR_SETTINGS = {
    'TITLE': PROJECT_TITLE,
    'DESCRIPTION': 'API description',
    'VERSION': '1.0.0',
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAdminUser'],
    'SERVE_AUTHENTICATION': ['rest_framework.authentication.SessionAuthentication'],
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'tryItOutEnabled': True,
        'displayRequestDuration': True,
        "persistAuthorization": True,
        'filter': True,
    },
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'Authorization': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'Bearer jwt token',
            },
            'Language': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Accept-Language',
                'description': 'Authorization by Token',
            },
        },
    },
    'SECURITY': [
        {'Authorization': [], 'Language': []},
    ],
}


if (SENTRY_DSN := os.environ.get('SENTRY_DSN')) and ENABLE_SENTRY:
    # More information on site https://sentry.io/
    from sentry_sdk import init
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.redis import RedisIntegration

    init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            RedisIntegration(),
            CeleryIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '1.0')),
        environment=os.environ.get('SENTRY_ENV', 'development'),
        sample_rate=float(os.environ.get('SENTRY_SAMPLE_RATE', '1.0')),
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
