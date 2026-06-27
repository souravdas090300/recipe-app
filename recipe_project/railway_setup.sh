#!/bin/bash
# ============================================================
# Railway Production Configuration Script
# Replaces: heroku_config_setup.sh
# Usage: bash railway_setup.sh
# Requires: Railway CLI — https://docs.railway.app/develop/cli
# ============================================================

set -e

echo "=================================="
echo "  Railway Production Configuration"
echo "=================================="
echo ""

# ── Check Railway CLI ────────────────────────────────────────
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Install it with:"
    echo "   npm install -g @railway/cli"
    echo "   OR: curl -fsSL https://railway.app/install.sh | sh"
    exit 1
fi
echo "✓ Railway CLI found"

# ── Login check ──────────────────────────────────────────────
if ! railway whoami &> /dev/null; then
    echo "⚠️  Not logged in. Running: railway login"
    railway login
fi
echo "✓ Logged in as: $(railway whoami)"
echo ""

# ── Link project ─────────────────────────────────────────────
echo "Linking to Railway project..."
echo "(A browser window will open — select your project)"
railway link
echo ""

# ── Generate SECRET_KEY ──────────────────────────────────────
echo "Generating Django SECRET_KEY..."
SECRET_KEY=$(python3 -c "
import secrets, string
chars = string.ascii_letters + string.digits + '!@#\$%^&*(-_=+)'
print(''.join(secrets.choice(chars) for _ in range(50)))
")
echo "✓ SECRET_KEY generated"

# ── Domain ───────────────────────────────────────────────────
echo ""
read -p "Enter your Railway domain (e.g., myapp.up.railway.app): " DOMAIN
if [ -z "$DOMAIN" ]; then
    echo "⚠️  No domain entered. You can set DJANGO_ALLOWED_HOSTS manually later."
    DOMAIN="localhost"
fi

# ── SSL ──────────────────────────────────────────────────────
echo ""
read -p "Enable HTTPS/SSL redirect? (y/n, recommended: y): " ENABLE_SSL
SSL_REDIRECT="true"
if [ "$ENABLE_SSL" != "y" ]; then
    SSL_REDIRECT="false"
fi

# ── AWS S3 ───────────────────────────────────────────────────
echo ""
read -p "Configure AWS S3 for media files? (y/n): " CONFIGURE_S3
USE_S3="false"
if [ "$CONFIGURE_S3" = "y" ]; then
    read -p "AWS Access Key ID: " AWS_KEY
    read -p "AWS Secret Access Key: " AWS_SECRET
    read -p "S3 Bucket Name: " S3_BUCKET
    read -p "S3 Region (default: us-east-1): " S3_REGION
    S3_REGION="${S3_REGION:-us-east-1}"
    USE_S3="true"
fi

# ── Set all variables ────────────────────────────────────────
echo ""
echo "Setting environment variables on Railway..."

railway variables set \
    DJANGO_SETTINGS_MODULE="config.settings.prod" \
    DJANGO_SECRET_KEY="$SECRET_KEY" \
    DJANGO_ALLOWED_HOSTS="$DOMAIN" \
    DJANGO_SECURE_SSL_REDIRECT="$SSL_REDIRECT" \
    DJANGO_CSRF_TRUSTED_ORIGINS="https://$DOMAIN" \
    PYTHON_VERSION="3.12" \
    USE_S3="$USE_S3"

if [ "$USE_S3" = "true" ]; then
    railway variables set \
        AWS_ACCESS_KEY_ID="$AWS_KEY" \
        AWS_SECRET_ACCESS_KEY="$AWS_SECRET" \
        AWS_STORAGE_BUCKET_NAME="$S3_BUCKET" \
        AWS_S3_REGION_NAME="$S3_REGION"
    echo "✓ AWS S3 variables set"
fi

echo ""
echo "✓ All variables set successfully"
echo ""

# ── Summary ──────────────────────────────────────────────────
echo "=================================="
echo "  Current Railway Variables"
echo "=================================="
railway variables
echo ""

echo "=================================="
echo "  Next Steps"
echo "=================================="
echo ""
echo "1. Add a PostgreSQL database in Railway dashboard:"
echo "   Dashboard → New → Database → PostgreSQL"
echo "   (DATABASE_URL is injected automatically)"
echo ""
echo "2. Deploy your app:"
echo "   railway up"
echo ""
echo "3. Run migrations (after first deploy):"
echo "   railway run python manage.py migrate --settings=config.settings.prod"
echo ""
echo "4. Create superuser:"
echo "   railway run python manage.py createsuperuser --settings=config.settings.prod"
echo ""
echo "5. View logs:"
echo "   railway logs"
echo ""
echo "6. Open your app:"
echo "   railway open"
echo ""
echo "See RAILWAY_DEPLOYMENT.md for full documentation."