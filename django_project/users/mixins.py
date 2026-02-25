from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(UserPassesTestMixin):
    """
    Mixin to restrict access based on user roles for class-based views.
    Usage: class MyView(RoleRequiredMixin, View):
               allowed_roles = ['admin', 'buyer']
    """
    allowed_roles = []

    def test_func(self):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            return self.request.user.profile.role in self.allowed_roles
        return False

class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin to restrict access to admin users only.
    """
    def test_func(self):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            return self.request.user.profile.is_admin()
        return False

class BuyerRequiredMixin(UserPassesTestMixin):
    """
    Mixin to restrict access to buyer and admin users.
    """
    def test_func(self):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            return self.request.user.profile.is_buyer() or self.request.user.profile.is_admin()
        return False
