# AWS S3 Setup Guide for Recipe App

This guide will walk you through setting up AWS S3 for media file storage in your Recipe App.

## Prerequisites
- AWS Account (you already have this ✓)
- Heroku CLI installed
- Access to your Heroku app

---

## Step 1: Create an S3 Bucket

1. **Log in to AWS Console**: https://console.aws.amazon.com/
2. **Navigate to S3**: Search for "S3" in the services search bar
3. **Create Bucket**:
   - Click **"Create bucket"**
   - **Bucket name**: `recipe-app-media-sourav` (must be globally unique)
   - **AWS Region**: Choose closest to you (e.g., `us-east-1`)
   - **Block Public Access settings**: 
     - ⚠️ **UNCHECK** "Block all public access"
     - Check the acknowledgment box
   - Click **"Create bucket"**

4. **Configure Bucket Policy**:
   - Go to your bucket → **Permissions** tab
   - Scroll to **Bucket Policy** → Click **Edit**
   - Paste this policy (replace `YOUR-BUCKET-NAME` with your actual bucket name):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
    ]
}
```

5. **Configure CORS**:
   - Go to **Permissions** tab → **CORS** section → Click **Edit**
   - Paste this configuration:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```

---

## Step 2: Create IAM User for Django

1. **Navigate to IAM**: Search for "IAM" in AWS services
2. **Create User**:
   - Click **Users** → **Add users**
   - **User name**: `django-s3-user`
   - Click **Next**
3. **Set Permissions**:
   - Select **Attach policies directly**
   - Search and select: **AmazonS3FullAccess**
   - Click **Next** → **Create user**
4. **Create Access Keys**:
   - Click on the newly created user
   - Go to **Security credentials** tab
   - Click **Create access key**
   - Select **Application running outside AWS**
   - Click **Next** → **Create access key**
   - ⚠️ **IMPORTANT**: Copy both:
     - **Access key ID** (e.g., `AKIAIOSFODNN7EXAMPLE`)
     - **Secret access key** (e.g., `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)
   - **Save these securely** - you won't see the secret key again!

---

## Step 3: Configure Heroku Environment Variables

Run these commands in your terminal (replace with your actual values):

```powershell
# Enable S3
heroku config:set USE_S3=true --app recipe-app-cf-sourav

# AWS Credentials
heroku config:set AWS_ACCESS_KEY_ID=your-access-key-id --app recipe-app-cf-sourav
heroku config:set AWS_SECRET_ACCESS_KEY=your-secret-access-key --app recipe-app-cf-sourav

# Bucket Configuration
heroku config:set AWS_STORAGE_BUCKET_NAME=recipe-app-media-sourav --app recipe-app-cf-sourav
heroku config:set AWS_S3_REGION_NAME=us-east-1 --app recipe-app-cf-sourav
```

**Example with actual values**:
```powershell
heroku config:set USE_S3=true --app recipe-app-cf-sourav
heroku config:set AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE --app recipe-app-cf-sourav
heroku config:set AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY --app recipe-app-cf-sourav
heroku config:set AWS_STORAGE_BUCKET_NAME=recipe-app-media-sourav --app recipe-app-cf-sourav
heroku config:set AWS_S3_REGION_NAME=us-east-1 --app recipe-app-cf-sourav
```

---

## Step 4: Verify Configuration

Check that all environment variables are set:
```powershell
heroku config --app recipe-app-cf-sourav
```

You should see:
```
USE_S3:                    true
AWS_ACCESS_KEY_ID:         AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY:     wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_STORAGE_BUCKET_NAME:   recipe-app-media-sourav
AWS_S3_REGION_NAME:        us-east-1
```

---

## Step 5: Deploy to Heroku

The code is already configured. Just commit and deploy:

```powershell
git add .
git commit -m "AWS S3: Add configuration for media file storage"
git push origin main
git push heroku main
```

---

## Step 6: Test the Integration

1. **Upload an image via admin**:
   - Go to: https://recipe-app-cf-sourav-d5b3ff514bd4.herokuapp.com/admin/
   - Edit a recipe and upload an image
   - Save the recipe

2. **Check S3 Bucket**:
   - Go to your S3 bucket in AWS Console
   - You should see a new folder: `media/recipes/`
   - The uploaded image should be there

3. **Verify on website**:
   - View the recipe detail page
   - The image should now load from S3 (check the image URL - it should be `https://recipe-app-media-sourav.s3.amazonaws.com/media/recipes/...`)

---

## Troubleshooting

### Images not uploading?
- Check Heroku logs: `heroku logs --tail --app recipe-app-cf-sourav`
- Verify AWS credentials are correct
- Ensure bucket policy allows public read access

### Images not displaying?
- Check the image URL in browser developer tools
- Verify CORS configuration in S3
- Check bucket is publicly accessible

### Access Denied errors?
- Verify IAM user has S3 full access permissions
- Check bucket policy is correctly configured

---

## Important Notes

⚠️ **Security**:
- Never commit AWS credentials to GitHub
- Always use environment variables (Heroku Config Vars)
- Regularly rotate access keys

💰 **AWS Costs**:
- S3 has a generous free tier (5GB storage, 20,000 GET requests/month)
- Monitor usage: https://console.aws.amazon.com/billing/

🔄 **Existing Images**:
- Images uploaded before S3 setup will need to be re-uploaded
- They're stored in Heroku's ephemeral filesystem and will be lost on dyno restart

---

## What's Been Configured

✅ Added packages to `requirements/prod.txt`:
- `boto3==1.35.71` (AWS SDK)
- `django-storages==1.14.4` (Django S3 integration)

✅ Updated `config/settings/base.py`:
- Added `storages` to `INSTALLED_APPS`

✅ Updated `config/settings/prod.py`:
- AWS S3 configuration
- Conditional S3 usage based on `USE_S3` environment variable
- Automatic media file routing to S3

---

## Next Steps

After completing this setup:
1. Deploy the changes to Heroku
2. Test by uploading a recipe image via admin
3. Verify the image appears in S3 bucket
4. Check the recipe detail page displays the image

Need help? Let me know at which step you're stuck!
