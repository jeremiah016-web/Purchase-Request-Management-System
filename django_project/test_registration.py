#!/usr/bin/env python
"""
Test script to verify registration functionality
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
from users.forms import UserRegistrationForm

def test_registration():
    print("Testing Registration Form...")
    print("=" * 60)
    
    # Test form data
    form_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'role': 'requester',
        'password1': 'TestPass123!',
        'password2': 'TestPass123!',
    }
    
    # Create form
    form = UserRegistrationForm(data=form_data)
    
    print(f"Form is valid: {form.is_valid()}")
    
    if not form.is_valid():
        print("\nForm Errors:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
        return False
    
    # Check if user already exists
    if User.objects.filter(username='testuser').exists():
        print("\nTest user already exists. Deleting...")
        User.objects.filter(username='testuser').delete()
    
    # Save user
    user = form.save()
    print(f"\n✓ User created: {user.username}")
    
    # Check profile
    if hasattr(user, 'profile'):
        print(f"✓ Profile exists")
        print(f"  - Role: {user.profile.role}")
        print(f"  - Image: {user.profile.image}")
    else:
        print("✗ Profile not created!")
        return False
    
    # Update profile role
    user.profile.role = form_data['role']
    user.profile.save()
    print(f"✓ Profile role updated to: {user.profile.role}")
    
    print("\n" + "=" * 60)
    print("Registration test PASSED! ✓")
    print("=" * 60)
    
    # Cleanup
    user.delete()
    print("\nTest user cleaned up.")
    
    return True

if __name__ == '__main__':
    try:
        test_registration()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
