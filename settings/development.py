
from decouple import config
import os


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'thunder_shack',
        'USER': config('DATABASES_USER'),
        'PASSWORD': config('DATABASES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',

    }
}

<<<<<<< HEAD
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587


#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
=======

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
>>>>>>> dc54500bfd7d097a06bc1acf1c5424f88895ec5c


# >> AWS S3 storage
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
