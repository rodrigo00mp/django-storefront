from .common import *
import os
load_dotenv(override=True)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['rmp-ecomm-prod-ae9dff4c41c3.herokuapp.com']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']
