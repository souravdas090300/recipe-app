from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# In real production, use environment variable and DO NOT hardcode secrets.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Replace with your actual domain(s) or server IP(s)
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# For real production, consider PostgreSQL/MySQL. SQLite kept for simplicity.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

