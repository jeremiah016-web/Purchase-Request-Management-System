from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from .models import Profile

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        if commit:
            user.save()
            # Create profile with role if it doesn't exist
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user, role='requester')
        return user

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        """
        pass

    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login user.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Get or create profile with default role
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'role': 'requester'}
        )
        
        # If user selected a role during signup, update it
        if hasattr(request, 'session') and 'signup_role' in request.session:
            profile.role = request.session.get('signup_role')
            profile.save()
            del request.session['signup_role']
        
        return user

    def populate_user(self, request, sociallogin, data):
        """
        Populate user information from social provider data.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Extract additional info from Google
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            if not user.first_name and 'given_name' in extra_data:
                user.first_name = extra_data.get('given_name', '')
            if not user.last_name and 'family_name' in extra_data:
                user.last_name = extra_data.get('family_name', '')
        
        return user
