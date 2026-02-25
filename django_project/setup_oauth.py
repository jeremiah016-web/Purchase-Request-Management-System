#!/usr/bin/env python
"""
Quick setup script for Google OAuth
Run this after configuring your Google Cloud credentials
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_oauth():
    print("=" * 60)
    print("Google OAuth Setup for PR Management System")
    print("=" * 60)
    print()
    
    # Check if site exists
    site, created = Site.objects.get_or_create(
        pk=1,
        defaults={
            'domain': 'localhost:8000',
            'name': 'PR Management System'
        }
    )
    
    if created:
        print("✓ Created site: localhost:8000")
    else:
        print(f"✓ Site already exists: {site.domain}")
    
    print()
    print("Please enter your Google OAuth credentials:")
    print("(You can find these in Google Cloud Console)")
    print()
    
    client_id = input("Google Client ID: ").strip()
    client_secret = input("Google Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("\n❌ Error: Client ID and Secret are required!")
        return
    
    # Create or update social app
    social_app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google OAuth',
            'client_id': client_id,
            'secret': client_secret,
        }
    )
    
    if not created:
        social_app.client_id = client_id
        social_app.secret = client_secret
        social_app.save()
        print("\n✓ Updated existing Google OAuth app")
    else:
        print("\n✓ Created new Google OAuth app")
    
    # Add site to social app
    social_app.sites.add(site)
    
    print("\n" + "=" * 60)
    print("Setup Complete! 🎉")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://localhost:8000/register/")
    print("3. Click 'Google' button to test OAuth login")
    print()
    print("For production deployment, see GOOGLE_OAUTH_SETUP.md")
    print()

if __name__ == '__main__':
    try:
        setup_oauth()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you've run migrations first:")
        print("python manage.py migrate")
