# Google OAuth Setup Guide

This guide will help you set up Google OAuth authentication for your Django PR Management System.

## Prerequisites

- A Google account
- Your Django project running locally or on a server

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on "Select a project" at the top
3. Click "New Project"
4. Enter a project name (e.g., "PR Management System")
5. Click "Create"

## Step 2: Enable Google+ API

1. In your Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google+ API"
3. Click on it and press "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields:
     - App name: PR Management System
     - User support email: your email
     - Developer contact: your email
   - Click "Save and Continue"
   - Skip the Scopes section (click "Save and Continue")
   - Add test users if needed
   - Click "Save and Continue"

4. Create OAuth Client ID:
   - Application type: "Web application"
   - Name: "PR Management System Web Client"
   - Authorized JavaScript origins:
     - http://localhost:8000
     - http://127.0.0.1:8000
     - (Add your production domain when deploying)
   - Authorized redirect URIs:
     - http://localhost:8000/accounts/google/login/callback/
     - http://127.0.0.1:8000/accounts/google/login/callback/
     - (Add your production domain when deploying)
   - Click "Create"

5. Copy your Client ID and Client Secret

## Step 4: Configure Django Settings

### Option A: Using Environment Variables (Recommended for Production)

1. Create a `.env` file in your project root:
```bash
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
```

2. Install python-decouple:
```bash
pip install python-decouple
```

3. The settings.py is already configured to read from environment variables

### Option B: Direct Configuration (For Development Only)

Edit `django_project/settings.py` and update the SOCIALACCOUNT_PROVIDERS section:

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': 'YOUR_CLIENT_ID_HERE',
            'secret': 'YOUR_CLIENT_SECRET_HERE',
            'key': ''
        }
    }
}
```

## Step 5: Run Migrations

```bash
cd django_project
python manage.py migrate
```

## Step 6: Add Social Application in Django Admin

1. Start your Django server:
```bash
python manage.py runserver
```

2. Go to http://localhost:8000/admin/

3. Log in with your superuser account (create one if needed):
```bash
python manage.py createsuperuser
```

4. Navigate to "Sites" and ensure you have a site with:
   - Domain name: localhost:8000 (or your domain)
   - Display name: PR Management System

5. Navigate to "Social applications" > "Add social application"

6. Fill in the form:
   - Provider: Google
   - Name: Google OAuth
   - Client id: (paste your Google Client ID)
   - Secret key: (paste your Google Client Secret)
   - Sites: Select your site and move it to "Chosen sites"
   - Click "Save"

## Step 7: Test Google Login

1. Go to http://localhost:8000/register/
2. Click the "Google" button
3. You should be redirected to Google's login page
4. After authentication, you'll be redirected back to your app
5. Select your role (Admin, Buyer, or Requester)
6. Complete the signup process

## Troubleshooting

### Error: redirect_uri_mismatch

- Make sure your redirect URI in Google Console exactly matches:
  `http://localhost:8000/accounts/google/login/callback/`
- Check for trailing slashes
- Ensure the protocol (http/https) matches

### Error: Social application not found

- Make sure you've added the Social Application in Django admin
- Verify the Client ID and Secret are correct
- Check that the site is properly configured

### Users can't select role after Google signup

- The role selection happens automatically after first Google login
- If users skip it, they can update their role in the profile page

## Production Deployment

When deploying to production:

1. Update Authorized JavaScript origins and redirect URIs in Google Console
2. Use environment variables for credentials (never commit secrets to git)
3. Set `DEBUG = False` in settings.py
4. Update `ALLOWED_HOSTS` in settings.py
5. Use HTTPS for all OAuth redirects

## Security Notes

- Never commit your Client ID and Secret to version control
- Use environment variables or secure secret management
- Regularly rotate your OAuth credentials
- Monitor OAuth usage in Google Cloud Console
- Enable 2FA for your Google Cloud account

## Additional Features

### Disconnect Google Account

Users can disconnect their Google account from their profile page.

### Multiple Social Providers

You can add more providers (GitHub, Facebook, etc.) by:
1. Installing the provider in INSTALLED_APPS
2. Configuring credentials in settings.py
3. Adding the provider in Django admin

## Support

For more information, visit:
- [django-allauth documentation](https://django-allauth.readthedocs.io/)
- [Google OAuth 2.0 documentation](https://developers.google.com/identity/protocols/oauth2)
