"""
Test script to verify AWS S3 connection and configuration.
Run this script to check if your S3 setup is working correctly.

Usage:
    python manage.py shell < test_s3_connection.py
    OR
    python test_s3_connection.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
django.setup()

from django.core.files.storage import default_storage
from django.conf import settings

def test_s3_connection():
    """Test S3 connection and configuration."""
    print("=" * 60)
    print("S3 Connection Test")
    print("=" * 60)
    
    # Check if S3 is enabled
    use_s3 = getattr(settings, 'USE_S3', False)
    print(f"\n1. USE_S3 setting: {use_s3}")
    
    if not use_s3:
        print("   ⚠️  S3 is NOT enabled. Set USE_S3=true in environment variables.")
        return False
    
    # Check AWS credentials
    print("\n2. AWS Configuration:")
    print(f"   - AWS_ACCESS_KEY_ID: {'✓ Set' if hasattr(settings, 'AWS_ACCESS_KEY_ID') else '✗ Missing'}")
    print(f"   - AWS_SECRET_ACCESS_KEY: {'✓ Set' if hasattr(settings, 'AWS_SECRET_ACCESS_KEY') else '✗ Missing'}")
    print(f"   - AWS_STORAGE_BUCKET_NAME: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '✗ Missing')}")
    print(f"   - AWS_S3_REGION_NAME: {getattr(settings, 'AWS_S3_REGION_NAME', '✗ Missing')}")
    print(f"   - AWS_S3_CUSTOM_DOMAIN: {getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', '✗ Missing')}")
    
    # Check storage backend
    print("\n3. Storage Backend:")
    print(f"   - DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', '✗ Missing')}")
    print(f"   - MEDIA_URL: {getattr(settings, 'MEDIA_URL', '✗ Missing')}")
    
    # Test storage connection
    print("\n4. Testing Storage Connection:")
    try:
        storage_class = default_storage.__class__.__name__
        print(f"   - Storage class: {storage_class}")
        
        # Test if we can list files (basic connectivity test)
        try:
            files = list(default_storage.listdir(''))[1][:5]  # Get first 5 files
            print(f"   - ✓ Can list files: Found {len(files)} files in bucket")
        except Exception as e:
            print(f"   - ⚠️  Cannot list files: {e}")
            print(f"   - This might be normal if bucket is empty")
        
        # Test file upload
        print("\n5. Testing File Upload:")
        try:
            test_filename = 'test_s3_upload.txt'
            test_content = b'S3 connection test - ' + str(os.urandom(16))
            
            # Upload test file
            default_storage.save(test_filename, test_content)
            print(f"   - ✓ Successfully uploaded test file: {test_filename}")
            
            # Test file download
            downloaded = default_storage.open(test_filename).read()
            if downloaded == test_content:
                print(f"   - ✓ Successfully downloaded and verified test file")
            else:
                print(f"   - ✗ Downloaded content doesn't match")
            
            # Clean up test file
            default_storage.delete(test_filename)
            print(f"   - ✓ Successfully deleted test file")
            
            print("\n" + "=" * 60)
            print("✓ S3 connection is working correctly!")
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"   - ✗ File upload failed: {e}")
            print(f"   - Error type: {type(e).__name__}")
            return False
            
    except Exception as e:
        print(f"   - ✗ Storage connection failed: {e}")
        print(f"   - Error type: {type(e).__name__}")
        return False

if __name__ == '__main__':
    success = test_s3_connection()
    sys.exit(0 if success else 1)
