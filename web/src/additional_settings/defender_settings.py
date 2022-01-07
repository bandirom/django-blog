from os import environ


DEFENDER_REDIS_URL = environ.get('REDIS_URL', 'redis://redis:6379') + '/1'
DEFENDER_USE_CELERY = False
DEFENDER_LOGIN_FAILURE_LIMIT = 3
DEFENDER_REDIS_NAME = 'default'
