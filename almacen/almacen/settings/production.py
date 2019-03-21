from .base import *

DEBUG = False

SECRET_KEY = 'llavesecretadeproduccion'

ALLOWED_HOSTS = ['.bla.com.mx']
SECRET_KEY = ['algoporaquicomotest']

MEDIA_URL = ''
MEDIA_ROOT = ''


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.production.sqlite3'),
    }
}


try:
    from .local import *
except ImportError:
    pass
