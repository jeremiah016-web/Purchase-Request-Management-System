from django.shortcuts import render, redirect
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from .models import Profile

def google_signup_role_selection(request):
    """
    View to allow users to select their role after Google OAuth signup
    """
    if request.method == 'POST':
        role = request.POST.get('role', 'requester')
        
        # Store role in session for the adapter to use
        request.session['signup_role'] = role
        
        # Redirect to Google OAuth
        return redirect('google_login')
    
    return render(request, 'users/google_role_selection.html')

def complete_social_signup(request):
    """
    Complete social signup by ensuring profile has a role
    """
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            if not request.user.profile.role or request.user.profile.role == '':
                # Show role selection form
                if request.method == 'POST':
                    role = request.POST.get('role', 'requester')
                    request.user.profile.role = role
                    request.user.profile.save()
                    messages.success(request, f'Welcome! Your account has been set up as {role}.')
                    return redirect('prs-home')
                
                return render(request, 'users/complete_social_signup.html')
        else:
            # Create profile if it doesn't exist
            Profile.objects.create(user=request.user, role='requester')
    
    return redirect('prs-home')
