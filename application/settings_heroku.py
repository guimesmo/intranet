from .settings import *
import os


DEBUG = False

ALLOWED_HOSTS = ['intranetlgsilva.herokuapp.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["DB_NAME"],
        'USER': os.environ["DB_USER"],
        'HOST': os.environ["DB_HOST"],
        'PASSWORD': os.environ["DB_PASSWORD"],
        'PORT': os.environ['DB_PORT']
    }
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]