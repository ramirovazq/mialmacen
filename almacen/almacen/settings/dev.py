from .base import *

DEBUG = True

SECRET_KEY = '_g(^)5qgms@+y0)*1kz)2pntjhalm8$0+%8^67^x0#agw+=3f-'

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/rvazquez/codigo/personal/mialmacen/almacen/uploads/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.dev.sqlite3'),
    }
}

try:
    from .local import *
except ImportError:
    pass

