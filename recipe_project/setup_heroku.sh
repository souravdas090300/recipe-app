#!/bin/bash
# Heroku Configuration Setup Script
# Run this script to configure all required environment variables for production

echo "=================================="
echo "Heroku Production Configuration"
echo "=================================="
echo ""

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✓ Heroku CLI found"
echo ""

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "⚠️  Not logged in to Heroku. Running login..."
    heroku login
fi

echo ""
echo "Current Heroku apps:"
heroku apps
echo ""

# Prompt for app name
read -p "Enter your Heroku app name: " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name is required"
    exit 1
fi

# Check if app exists
if ! heroku apps:info -a "$APP_NAME" &> /dev/null; then
    echo "❌ App '$APP_NAME' not found"
    echo ""
    read -p "Create new app? (y/n): " CREATE_APP
    if [ "$CREATE_APP" = "y" ]; then
        heroku create "$APP_NAME"
    else
        exit 1
    fi
fi

echo ""
echo "Configuring app: $APP_NAME"
echo ""

# Generate SECRET_KEY
echo "Generating Django SECRET_KEY..."
SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 2>/dev/null)

if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  Could not generate SECRET_KEY (Django not installed?)"
    echo "You'll need to set this manually:"
    echo "  heroku config:set DJANGO_SECRET_KEY='your-secret-key' -a $APP_NAME"
else
    echo "✓ SECRET_KEY generated"
    heroku config:set DJANGO_SECRET_KEY="$SECRET_KEY" -a "$APP_NAME"
fi

# Set Django settings module
echo ""
echo "Setting Django settings module..."
heroku config:set DJANGO_SETTINGS_MODULE="config.settings.prod" -a "$APP_NAME"

# Set allowed hosts
echo ""
read -p "Enter your domain (e.g., $APP_NAME.herokuapp.com): " DOMAIN
if [ -z "$DOMAIN" ]; then
    DOMAIN="$APP_NAME.herokuapp.com"
fi

echo "Setting ALLOWED_HOSTS to: $DOMAIN"
heroku config:set DJANGO_ALLOWED_HOSTS="$DOMAIN" -a "$APP_NAME"

# Security settings
echo ""
read -p "Enable SSL security (HTTPS)? Recommended after first deployment (y/n): " ENABLE_SSL

if [ "$ENABLE_SSL" = "y" ]; then
    echo "Enabling SSL security settings..."
    heroku config:set DJANGO_SECURE_SSL_REDIRECT="true" -a "$APP_NAME"
    heroku config:set DJANGO_SESSION_COOKIE_SECURE="true" -a "$APP_NAME"
    heroku config:set DJANGO_CSRF_COOKIE_SECURE="true" -a "$APP_NAME"
    heroku config:set DJANGO_CSRF_TRUSTED_ORIGINS="https://$DOMAIN" -a "$APP_NAME"
else
    echo "⚠️  SSL security disabled. Enable it after first deployment."
    heroku config:set DJANGO_SECURE_SSL_REDIRECT="false" -a "$APP_NAME"
    heroku config:set DJANGO_SESSION_COOKIE_SECURE="false" -a "$APP_NAME"
    heroku config:set DJANGO_CSRF_COOKIE_SECURE="false" -a "$APP_NAME"
fi

# Database
echo ""
echo "Checking for PostgreSQL addon..."
if heroku addons:info heroku-postgresql -a "$APP_NAME" &> /dev/null; then
    echo "✓ PostgreSQL already configured"
else
    read -p "Add PostgreSQL database? (y/n): " ADD_DB
    if [ "$ADD_DB" = "y" ]; then
        heroku addons:create heroku-postgresql:mini -a "$APP_NAME"
        echo "✓ PostgreSQL added"
    fi
fi

# AWS S3
echo ""
read -p "Configure AWS S3 for media files? (y/n): " CONFIGURE_S3

if [ "$CONFIGURE_S3" = "y" ]; then
    echo ""
    echo "AWS S3 Configuration"
    echo "Get these from AWS IAM Console: https://console.aws.amazon.com/iam/"
    echo ""
    
    read -p "AWS Access Key ID: " AWS_KEY
    read -p "AWS Secret Access Key: " AWS_SECRET
    read -p "S3 Bucket Name: " S3_BUCKET
    read -p "S3 Region (e.g., us-east-1): " S3_REGION
    
    if [ -n "$AWS_KEY" ] && [ -n "$AWS_SECRET" ] && [ -n "$S3_BUCKET" ]; then
        heroku config:set USE_S3="true" -a "$APP_NAME"
        heroku config:set AWS_ACCESS_KEY_ID="$AWS_KEY" -a "$APP_NAME"
        heroku config:set AWS_SECRET_ACCESS_KEY="$AWS_SECRET" -a "$APP_NAME"
        heroku config:set AWS_STORAGE_BUCKET_NAME="$S3_BUCKET" -a "$APP_NAME"
        heroku config:set AWS_S3_REGION_NAME="${S3_REGION:-us-east-1}" -a "$APP_NAME"
        echo "✓ AWS S3 configured"
    else
        echo "⚠️  Incomplete S3 configuration. Skipping..."
    fi
else
    echo "⚠️  S3 not configured. Media files will use local storage."
fi

# Summary
echo ""
echo "=================================="
echo "Configuration Summary"
echo "=================================="
heroku config -a "$APP_NAME"

echo ""
echo "=================================="
echo "Next Steps"
echo "=================================="
echo ""
echo "1. Deploy your application:"
echo "   git push heroku main"
echo ""
echo "2. Run database migrations:"
echo "   heroku run python manage.py migrate --settings=config.settings.prod -a $APP_NAME"
echo ""
echo "3. Create superuser:"
echo "   heroku run python manage.py createsuperuser --settings=config.settings.prod -a $APP_NAME"
echo ""
echo "4. Collect static files:"
echo "   heroku run python manage.py collectstatic --noinput --settings=config.settings.prod -a $APP_NAME"
echo ""
echo "5. Open your application:"
echo "   heroku open -a $APP_NAME"
echo ""
echo "6. Monitor logs:"
echo "   heroku logs --tail -a $APP_NAME"
echo ""
echo "See DEPLOYMENT.md for more information."
