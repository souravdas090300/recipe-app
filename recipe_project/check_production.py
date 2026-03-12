#!/usr/bin/env python3
"""
Quick Production Configuration Checker
Verifies that all required environment variables and settings are properly configured.
"""

import os
import sys
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def check_item(condition, success_msg, failure_msg):
    """Check a condition and print colored result"""
    if condition:
        print(f"{GREEN}✓{RESET} {success_msg}")
        return True
    else:
        print(f"{RED}✗{RESET} {failure_msg}")
        return False


def check_warning(condition, warning_msg):
    """Print a warning if condition is met"""
    if condition:
        print(f"{YELLOW}⚠{RESET} {warning_msg}")


def main():
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}Production Configuration Checker{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

    all_checks_passed = True
    warnings = []

    # Check 1: Python Version
    print(f"\n{BLUE}1. Python Version{RESET}")
    runtime_file = Path(__file__).parent / 'runtime.txt'
    if runtime_file.exists():
        with open(runtime_file) as f:
            runtime_version = f.read().strip()
        check_item(
            'python-3.12' in runtime_version or 'python-3.11' in runtime_version,
            f"runtime.txt: {runtime_version}",
            f"runtime.txt: {runtime_version} (may not be supported by Heroku)"
        )
    else:
        check_item(False, "", "runtime.txt not found")
        all_checks_passed = False

    # Check 2: Required Files
    print(f"\n{BLUE}2. Required Files{RESET}")
    required_files = {
        'Procfile': 'Procfile for Heroku deployment',
        'requirements/prod.txt': 'Production requirements',
        'config/settings/prod.py': 'Production settings',
        'config/wsgi.py': 'WSGI configuration',
    }
    
    for file_path, description in required_files.items():
        full_path = Path(__file__).parent / file_path
        if not check_item(
            full_path.exists(),
            f"{description}: {file_path}",
            f"{description}: {file_path} NOT FOUND"
        ):
            all_checks_passed = False

    # Check 3: Environment Variables (if Django is available)
    print(f"\n{BLUE}3. Environment Variables (Required for Production){RESET}")
    try:
        # Try to import Django settings (this will only work if Django is installed)
        sys.path.insert(0, str(Path(__file__).parent))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
        
        try:
            import django
            django.setup()
            from django.conf import settings
            
            # Check SECRET_KEY
            if settings.SECRET_KEY and len(settings.SECRET_KEY) >= 50:
                if settings.SECRET_KEY == 'change-this-in-production':
                    check_item(False, "", "SECRET_KEY not changed from default")
                    all_checks_passed = False
                else:
                    check_item(True, "SECRET_KEY is set and secure", "")
            else:
                check_item(False, "", "SECRET_KEY is too short or not set")
                all_checks_passed = False
            
            # Check DEBUG
            check_item(
                not settings.DEBUG,
                "DEBUG is False",
                "DEBUG is True (DANGEROUS in production!)"
            )
            if settings.DEBUG:
                all_checks_passed = False
            
            # Check ALLOWED_HOSTS
            if settings.ALLOWED_HOSTS == ['*']:
                check_warning(True, "ALLOWED_HOSTS uses wildcard '*' (should be specific domains)")
                warnings.append("Set specific ALLOWED_HOSTS")
            elif settings.ALLOWED_HOSTS:
                check_item(True, f"ALLOWED_HOSTS configured: {', '.join(settings.ALLOWED_HOSTS)}", "")
            else:
                check_item(False, "", "ALLOWED_HOSTS is empty")
                all_checks_passed = False
            
            # Check Database
            db_config = settings.DATABASES.get('default', {})
            if 'postgresql' in db_config.get('ENGINE', ''):
                check_item(True, "Database: PostgreSQL", "")
            elif 'sqlite3' in db_config.get('ENGINE', ''):
                check_warning(True, "Database: SQLite (use PostgreSQL in production)")
                warnings.append("Use PostgreSQL for production")
            
            # Check Static Files
            check_item(
                'whitenoise' in str(settings.MIDDLEWARE).lower(),
                "WhiteNoise configured for static files",
                "WhiteNoise not found in MIDDLEWARE"
            )
            
            # Check S3
            if hasattr(settings, 'USE_S3') and settings.USE_S3:
                s3_configured = all([
                    settings.AWS_ACCESS_KEY_ID,
                    settings.AWS_SECRET_ACCESS_KEY,
                    settings.AWS_STORAGE_BUCKET_NAME
                ])
                check_item(
                    s3_configured,
                    "AWS S3 configured for media files",
                    "AWS S3 enabled but credentials incomplete"
                )
            else:
                check_warning(True, "AWS S3 not enabled (recommended for media files)")
                warnings.append("Consider enabling AWS S3 for media files")
            
            # Check Security Settings
            print(f"\n{BLUE}4. Security Settings{RESET}")
            
            security_checks = {
                'SECURE_SSL_REDIRECT': settings.SECURE_SSL_REDIRECT,
                'SESSION_COOKIE_SECURE': settings.SESSION_COOKIE_SECURE,
                'CSRF_COOKIE_SECURE': settings.CSRF_COOKIE_SECURE,
            }
            
            for setting_name, value in security_checks.items():
                if value:
                    check_item(True, f"{setting_name} enabled", "")
                else:
                    check_warning(True, f"{setting_name} disabled (enable after SSL is configured)")
            
            # Check CSRF Trusted Origins
            if hasattr(settings, 'CSRF_TRUSTED_ORIGINS'):
                if settings.CSRF_TRUSTED_ORIGINS:
                    check_item(True, f"CSRF_TRUSTED_ORIGINS configured", "")
                else:
                    check_warning(True, "CSRF_TRUSTED_ORIGINS not set (may cause CSRF errors)")
                    warnings.append("Set CSRF_TRUSTED_ORIGINS")
            
        except ImportError:
            print(f"{YELLOW}⚠{RESET} Django not installed - skipping settings check")
            print(f"  To check Django settings, activate your virtual environment first")
        except Exception as e:
            print(f"{YELLOW}⚠{RESET} Could not load Django settings: {e}")
            print(f"  This is normal if environment variables are not set locally")
    
    except Exception as e:
        print(f"{YELLOW}⚠{RESET} Could not check Django configuration: {e}")

    # Check 5: Procfile
    print(f"\n{BLUE}5. Procfile Configuration{RESET}")
    procfile = Path(__file__).parent / 'Procfile'
    if procfile.exists():
        with open(procfile) as f:
            content = f.read().strip()
        if 'gunicorn' in content:
            check_item(True, f"Procfile uses gunicorn: {content}", "")
        else:
            check_item(False, "", f"Procfile doesn't use gunicorn: {content}")
            all_checks_passed = False
    else:
        check_item(False, "", "Procfile not found")
        all_checks_passed = False

    # Check 6: .gitignore
    print(f"\n{BLUE}6. Git Configuration{RESET}")
    gitignore = Path(__file__).parent.parent / '.gitignore'
    if gitignore.exists():
        with open(gitignore) as f:
            gitignore_content = f.read()
        
        checks = [
            ('.env' in gitignore_content, ".env files ignored"),
            ('db.sqlite3' in gitignore_content, "SQLite database ignored"),
            ('*.log' in gitignore_content, "Log files ignored"),
        ]
        
        for condition, msg in checks:
            check_item(condition, msg, f"{msg} - NOT FOUND")
    else:
        check_warning(True, ".gitignore not found")

    # Summary
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"\n{BLUE}Summary{RESET}")
    print(f"{BLUE}{'='*70}{RESET}")
    
    if all_checks_passed and not warnings:
        print(f"\n{GREEN}✓ All checks passed! Ready for production deployment.{RESET}\n")
    elif all_checks_passed and warnings:
        print(f"\n{YELLOW}⚠ Configuration is acceptable but has warnings:{RESET}")
        for warning in set(warnings):
            print(f"  • {warning}")
        print()
    else:
        print(f"\n{RED}✗ Some critical checks failed. Please fix issues before deploying.{RESET}\n")
    
    print(f"{BLUE}Next Steps:{RESET}")
    print(f"1. Set environment variables in Heroku:")
    print(f"   heroku config:set DJANGO_SECRET_KEY='your-secret-key'")
    print(f"   heroku config:set DJANGO_ALLOWED_HOSTS='your-domain.herokuapp.com'")
    print(f"")
    print(f"2. Deploy to Heroku:")
    print(f"   git push heroku main")
    print(f"")
    print(f"3. Run migrations:")
    print(f"   heroku run python manage.py migrate --settings=config.settings.prod")
    print(f"")
    print(f"4. Create superuser:")
    print(f"   heroku run python manage.py createsuperuser --settings=config.settings.prod")
    print(f"")
    print(f"See DEPLOYMENT.md for complete instructions.\n")


if __name__ == '__main__':
    main()
