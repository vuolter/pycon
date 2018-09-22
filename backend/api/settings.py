from django.conf import settings

LIMIT_MAX_VALUE = settings.API_SETTINGS['PAGINATION']['LIMIT_MAX_VALUE']
LIMIT_MIN_VALUE = settings.API_SETTINGS['PAGINATION']['LIMIT_MIN_VALUE']
LIMIT_DEFAULT_VALUE = settings.API_SETTINGS['PAGINATION']['LIMIT_DEFAULT_VALUE']