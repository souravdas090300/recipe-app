import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
django.setup()

from django.contrib.auth.models import User

# List all superusers
superusers = User.objects.filter(is_superuser=True)
print("\n=== SUPERUSERS ON HEROKU ===")
if superusers.exists():
    for user in superusers:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Active: {user.is_active}")
        print(f"Staff: {user.is_staff}")
        print(f"Superuser: {user.is_superuser}")
        print("-" * 40)
else:
    print("No superusers found!")

# Check if souravdas09300 exists
try:
    user = User.objects.get(username='souravdas09300')
    print("\n=== USER 'souravdas09300' EXISTS ===")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Active: {user.is_active}")
    print(f"Staff: {user.is_staff}")
    print(f"Superuser: {user.is_superuser}")
except User.DoesNotExist:
    print("\n=== USER 'souravdas09300' NOT FOUND ===")
    print("This user does not exist in the database.")
