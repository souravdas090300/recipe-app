#!/usr/bin/env python
"""Test S3 connection and upload"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

print("=" * 60)
print("S3 Configuration Test")
print("=" * 60)

# Check storage backend
print(f"\n1. Storage Backend: {type(default_storage).__name__}")
print(f"   Module: {type(default_storage).__module__}")

# Check if it's S3
if hasattr(default_storage, 'bucket_name'):
    print(f"\n2. S3 Bucket: {default_storage.bucket_name}")
    print(f"   Region: {getattr(default_storage, 'region_name', 'Not set')}")
else:
    print("\n2. NOT using S3 storage!")
    exit(1)

# Test connection
print("\n3. Testing S3 connection...")
try:
    # Try to save a test file
    test_file = ContentFile(b'This is a test file for S3 connection')
    filename = default_storage.save('test/connection_test.txt', test_file)
    print(f"   ✓ Successfully saved: {filename}")
    
    # Get the URL
    url = default_storage.url(filename)
    print(f"   ✓ File URL: {url}")
    
    # Delete test file
    default_storage.delete(filename)
    print(f"   ✓ Test file cleaned up")
    
    print("\n" + "=" * 60)
    print("✓ S3 CONNECTION WORKING!")
    print("=" * 60)
    
except Exception as e:
    print(f"   ✗ ERROR: {str(e)}")
    print(f"   Type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 60)
    print("✗ S3 CONNECTION FAILED!")
    print("=" * 60)
    exit(1)
