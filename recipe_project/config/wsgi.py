"""
WSGI config for recipe_project project.

IMPORTANT: This file is used for PRODUCTION deployment.
- Uses settings.py (production settings) by default
- For local development servers, manage.py uses settings_local.py

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Production: Use explicit production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

application = get_wsgi_application()
