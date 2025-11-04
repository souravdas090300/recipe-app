#!/usr/bin/env python
"""
Script to delete superuser on Heroku
"""
import os
import sys
import django

# Add recipe_project to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'recipe_project'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Delete mentorCF user if exists
try:
    user = User.objects.get(username='mentorCF')
    user.delete()
    print("✅ Superuser 'mentorCF' has been deleted successfully!")
except User.DoesNotExist:
    print("ℹ️  Superuser 'mentorCF' does not exist.")
