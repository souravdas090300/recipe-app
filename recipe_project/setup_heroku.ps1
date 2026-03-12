# Heroku Configuration Setup Script (PowerShell)
# Run this script to configure all required environment variables for production

Write-Host "=================================="
Write-Host "Heroku Production Configuration"
Write-Host "=================================="
Write-Host ""

# Check if Heroku CLI is installed
try {
    $null = Get-Command heroku -ErrorAction Stop
    Write-Host "✓ Heroku CLI found" -ForegroundColor Green
}
catch {
    Write-Host "❌ Heroku CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
}

Write-Host ""

# Check if logged in to Heroku
try {
    heroku auth:whoami 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Not logged in to Heroku. Running login..." -ForegroundColor Yellow
        heroku login
    }
}
catch {
    Write-Host "⚠️  Not logged in to Heroku. Running login..." -ForegroundColor Yellow
    heroku login
}

Write-Host ""
Write-Host "Current Heroku apps:"
heroku apps
Write-Host ""

# Prompt for app name
$APP_NAME = Read-Host "Enter your Heroku app name"

if ([string]::IsNullOrWhiteSpace($APP_NAME)) {
    Write-Host "❌ App name is required" -ForegroundColor Red
    exit 1
}

# Check if app exists
heroku apps:info -a $APP_NAME 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ App '$APP_NAME' not found" -ForegroundColor Red
    Write-Host ""
    $CREATE_APP = Read-Host "Create new app? (y/n)"
    if ($CREATE_APP -eq "y") {
        heroku create $APP_NAME
    }
    else {
        exit 1
    }
}

Write-Host ""
Write-Host "Configuring app: $APP_NAME" -ForegroundColor Cyan
Write-Host ""

# Generate SECRET_KEY
Write-Host "Generating Django SECRET_KEY..."
try {
    $SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 2>$null
    
    if ([string]::IsNullOrWhiteSpace($SECRET_KEY)) {
        throw "Empty key"
    }
    
    Write-Host "✓ SECRET_KEY generated" -ForegroundColor Green
    heroku config:set "DJANGO_SECRET_KEY=$SECRET_KEY" -a $APP_NAME
}
catch {
    Write-Host "⚠️  Could not generate SECRET_KEY (Django not installed?)" -ForegroundColor Yellow
    Write-Host "You'll need to set this manually:"
    Write-Host "  heroku config:set DJANGO_SECRET_KEY='your-secret-key' -a $APP_NAME"
}

# Set Django settings module
Write-Host ""
Write-Host "Setting Django settings module..."
heroku config:set DJANGO_SETTINGS_MODULE="config.settings.prod" -a $APP_NAME

# Set allowed hosts
Write-Host ""
$DOMAIN = Read-Host "Enter your domain (e.g., $APP_NAME.herokuapp.com)"
if ([string]::IsNullOrWhiteSpace($DOMAIN)) {
    $DOMAIN = "$APP_NAME.herokuapp.com"
}

Write-Host "Setting ALLOWED_HOSTS to: $DOMAIN"
heroku config:set "DJANGO_ALLOWED_HOSTS=$DOMAIN" -a $APP_NAME

# Security settings
Write-Host ""
$ENABLE_SSL = Read-Host "Enable SSL security (HTTPS)? Recommended after first deployment (y/n)"

if ($ENABLE_SSL -eq "y") {
    Write-Host "Enabling SSL security settings..." -ForegroundColor Green
    heroku config:set DJANGO_SECURE_SSL_REDIRECT="true" -a $APP_NAME
    heroku config:set DJANGO_SESSION_COOKIE_SECURE="true" -a $APP_NAME
    heroku config:set DJANGO_CSRF_COOKIE_SECURE="true" -a $APP_NAME
    heroku config:set "DJANGO_CSRF_TRUSTED_ORIGINS=https://$DOMAIN" -a $APP_NAME
}
else {
    Write-Host "⚠️  SSL security disabled. Enable it after first deployment." -ForegroundColor Yellow
    heroku config:set DJANGO_SECURE_SSL_REDIRECT="false" -a $APP_NAME
    heroku config:set DJANGO_SESSION_COOKIE_SECURE="false" -a $APP_NAME
    heroku config:set DJANGO_CSRF_COOKIE_SECURE="false" -a $APP_NAME
}

# Database
Write-Host ""
Write-Host "Checking for PostgreSQL addon..."
heroku addons:info heroku-postgresql -a $APP_NAME 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ PostgreSQL already configured" -ForegroundColor Green
}
else {
    $ADD_DB = Read-Host "Add PostgreSQL database? (y/n)"
    if ($ADD_DB -eq "y") {
        heroku addons:create heroku-postgresql:mini -a $APP_NAME
        Write-Host "✓ PostgreSQL added" -ForegroundColor Green
    }
}

# AWS S3
Write-Host ""
$CONFIGURE_S3 = Read-Host "Configure AWS S3 for media files? (y/n)"

if ($CONFIGURE_S3 -eq "y") {
    Write-Host ""
    Write-Host "AWS S3 Configuration" -ForegroundColor Cyan
    Write-Host "Get these from AWS IAM Console: https://console.aws.amazon.com/iam/"
    Write-Host ""
    
    $AWS_KEY = Read-Host "AWS Access Key ID"
    $AWS_SECRET = Read-Host "AWS Secret Access Key"
    $S3_BUCKET = Read-Host "S3 Bucket Name"
    $S3_REGION = Read-Host "S3 Region (e.g., us-east-1)"
    
    if (-not [string]::IsNullOrWhiteSpace($AWS_KEY) -and 
        -not [string]::IsNullOrWhiteSpace($AWS_SECRET) -and 
        -not [string]::IsNullOrWhiteSpace($S3_BUCKET)) {
        
        heroku config:set USE_S3="true" -a $APP_NAME
        heroku config:set "AWS_ACCESS_KEY_ID=$AWS_KEY" -a $APP_NAME
        heroku config:set "AWS_SECRET_ACCESS_KEY=$AWS_SECRET" -a $APP_NAME
        heroku config:set "AWS_STORAGE_BUCKET_NAME=$S3_BUCKET" -a $APP_NAME
        
        if ([string]::IsNullOrWhiteSpace($S3_REGION)) {
            $S3_REGION = "us-east-1"
        }
        heroku config:set "AWS_S3_REGION_NAME=$S3_REGION" -a $APP_NAME
        
        Write-Host "✓ AWS S3 configured" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  Incomplete S3 configuration. Skipping..." -ForegroundColor Yellow
    }
}
else {
    Write-Host "⚠️  S3 not configured. Media files will use local storage." -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "=================================="
Write-Host "Configuration Summary"
Write-Host "=================================="
heroku config -a $APP_NAME

Write-Host ""
Write-Host "=================================="
Write-Host "Next Steps"
Write-Host "=================================="
Write-Host ""
Write-Host "1. Deploy your application:"
Write-Host "   git push heroku main" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Run database migrations:"
Write-Host "   heroku run python manage.py migrate --settings=config.settings.prod -a $APP_NAME" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Create superuser:"
Write-Host "   heroku run python manage.py createsuperuser --settings=config.settings.prod -a $APP_NAME" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Collect static files:"
Write-Host "   heroku run python manage.py collectstatic --noinput --settings=config.settings.prod -a $APP_NAME" -ForegroundColor Yellow
Write-Host ""
Write-Host "5. Open your application:"
Write-Host "   heroku open -a $APP_NAME" -ForegroundColor Yellow
Write-Host ""
Write-Host "6. Monitor logs:"
Write-Host "   heroku logs --tail -a $APP_NAME" -ForegroundColor Yellow
Write-Host ""
Write-Host "See DEPLOYMENT.md for more information." -ForegroundColor Cyan
