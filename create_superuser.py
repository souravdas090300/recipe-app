#!/usr/bin/env python
"""
Script to create superuser non-interactively on Heroku
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser if it doesn't exist
if not User.objects.filter(username='mentorCF').exists():
    User.objects.create_superuser(
        username='mentorCF',
        email='mentor@careerfoundry.com',
        password='Ment0r@CareerF0undry'
    )
    print("✅ Superuser 'mentorCF' created successfully!")
else:
    print("ℹ️  Superuser 'mentorCF' already exists.")
    # Update password for existing user
    user = User.objects.get(username='mentorCF')
    user.set_password('Ment0r@CareerF0undry')
    user.save()
    print("✅ Password updated for existing superuser.")
