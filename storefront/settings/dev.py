from .common import *
import os
load_dotenv(override=True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  'storefront3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': str(os.getenv('DB_PASSWORD'))
    }
}
