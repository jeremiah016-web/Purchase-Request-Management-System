from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorator to restrict access based on user roles.
    Usage: @role_required(['admin', 'buyer'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if hasattr(request.user, 'profile'):
                    if request.user.profile.role in allowed_roles:
                        return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator

def admin_required(view_func):
    """
    Decorator to restrict access to admin users only.
    Usage: @admin_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            if request.user.profile.is_admin():
                return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

def buyer_required(view_func):
    """
    Decorator to restrict access to buyer users only.
    Usage: @buyer_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            if request.user.profile.is_buyer() or request.user.profile.is_admin():
                return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper
