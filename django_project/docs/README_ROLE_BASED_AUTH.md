# Role-Based Authentication with Google OAuth

This Django PR Management System now includes role-based authentication with Google OAuth integration.

## Features

### 1. Role-Based Access Control
- **Admin**: Full system access, can delete PRs, manage all users
- **Buyer**: Can review and approve purchase requests, view buyer lists
- **Requester**: Can create and manage their own purchase requests

### 2. Authentication Methods
- Traditional email/password registration and login
- Google OAuth 2.0 authentication
- Automatic profile creation with role assignment

### 3. User Management
- Custom user profiles with role field
- Role selection during registration
- Role display in user profile
- Role-based view permissions

## Quick Start

### 1. Install Dependencies

```bash
cd django_project
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Set Up Google OAuth (Optional)

Follow the detailed guide in `GOOGLE_OAUTH_SETUP.md` or use the quick setup script:

```bash
python setup_oauth.py
```

### 5. Run the Server

```bash
python manage.py runserver
```

### 6. Access the Application

- Home: http://localhost:8000/
- Register: http://localhost:8000/register/
- Login: http://localhost:8000/login/
- Admin: http://localhost:8000/admin/

## File Structure

```
django_project/
├── users/
│   ├── models.py              # Profile model with role field
│   ├── forms.py               # Registration forms with role selection
│   ├── views.py               # User views (register, profile)
│   ├── social_views.py        # Google OAuth views
│   ├── adapters.py            # Custom allauth adapters
│   ├── decorators.py          # Role-based decorators
│   ├── mixins.py              # Role-based mixins for CBVs
│   ├── migrations/
│   │   └── 0003_profile_role.py
│   └── templates/
│       └── users/
│           ├── register.html
│           ├── login.html
│           ├── profile.html
│           └── complete_social_signup.html
├── prs/
│   ├── views.py               # Updated with role-based permissions
│   └── ...
├── django_project/
│   ├── settings.py            # Updated with allauth configuration
│   └── urls.py                # Added allauth URLs
├── requirements.txt
├── GOOGLE_OAUTH_SETUP.md
└── setup_oauth.py
```

## Usage Examples

### Using Role Decorators (Function-Based Views)

```python
from users.decorators import role_required, admin_required, buyer_required

@role_required(['admin', 'buyer'])
def some_view(request):
    # Only admins and buyers can access
    pass

@admin_required
def admin_only_view(request):
    # Only admins can access
    pass

@buyer_required
def buyer_view(request):
    # Buyers and admins can access
    pass
```

### Using Role Mixins (Class-Based Views)

```python
from users.mixins import RoleRequiredMixin, AdminRequiredMixin, BuyerRequiredMixin

class MyView(RoleRequiredMixin, ListView):
    allowed_roles = ['admin', 'buyer']
    model = MyModel

class AdminOnlyView(AdminRequiredMixin, UpdateView):
    model = MyModel

class BuyerView(BuyerRequiredMixin, DetailView):
    model = MyModel
```

### Checking Roles in Templates

```django
{% if user.profile.is_admin %}
    <a href="{% url 'admin-panel' %}">Admin Panel</a>
{% endif %}

{% if user.profile.is_buyer %}
    <a href="{% url 'buyer-dashboard' %}">Buyer Dashboard</a>
{% endif %}

<p>Your role: {{ user.profile.get_role_display }}</p>
```

### Checking Roles in Python

```python
if request.user.profile.is_admin():
    # Admin-specific logic
    pass

if request.user.profile.is_buyer():
    # Buyer-specific logic
    pass

if request.user.profile.role == 'requester':
    # Requester-specific logic
    pass
```

## Current Role Permissions

### Admin
- Create, read, update, and delete all PRs
- Access buyer list
- Manage all users
- Full system access

### Buyer
- Create and read PRs
- Update any PR (status, category, description)
- Access buyer list
- Cannot delete PRs

### Requester
- Create PRs
- Read all PRs
- Update only their own PRs
- Cannot delete PRs
- Cannot access buyer list

## Customization

### Adding New Roles

1. Update `ROLE_CHOICES` in `users/models.py`:
```python
ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('buyer', 'Buyer'),
    ('requester', 'Requester'),
    ('manager', 'Manager'),  # New role
)
```

2. Add helper methods in `Profile` model:
```python
def is_manager(self):
    return self.role == 'manager'
```

3. Create decorators/mixins if needed in `users/decorators.py` and `users/mixins.py`

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Modifying Permissions

Edit the `test_func` methods in views or create custom decorators/mixins.

Example in `prs/views.py`:
```python
def test_func(self):
    pr = self.get_object()
    # Custom permission logic
    if self.request.user.profile.is_admin():
        return True
    if self.request.user.profile.is_buyer() and pr.status == 'Pending':
        return True
    return self.request.user == pr.author
```

## Security Considerations

1. **Never commit secrets**: Use environment variables for OAuth credentials
2. **HTTPS in production**: Always use HTTPS for OAuth redirects
3. **Regular updates**: Keep django-allauth and Django updated
4. **Role validation**: Always validate roles on the backend, not just frontend
5. **Session security**: Configure secure session settings in production

## Environment Variables

Create a `.env` file (don't commit this):

```bash
# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Testing

### Test Role-Based Access

1. Create users with different roles
2. Try accessing restricted views
3. Verify permission denials work correctly

### Test Google OAuth

1. Click "Google" button on register/login page
2. Authenticate with Google
3. Select role on completion page
4. Verify profile is created with correct role

## Troubleshooting

### "Profile matching query does not exist"

Run this in Django shell:
```python
from django.contrib.auth.models import User
from users.models import Profile

for user in User.objects.all():
    Profile.objects.get_or_create(user=user, defaults={'role': 'requester'})
```

### Google OAuth not working

1. Check `GOOGLE_OAUTH_SETUP.md` for detailed setup
2. Verify redirect URIs in Google Console
3. Check Social Application in Django admin
4. Ensure migrations are run

### Permission denied errors

1. Check user has a profile: `user.profile`
2. Verify role is set: `user.profile.role`
3. Check view permissions in `views.py`

## Production Deployment

1. Set environment variables
2. Update `ALLOWED_HOSTS` in settings.py
3. Set `DEBUG = False`
4. Configure HTTPS
5. Update Google OAuth redirect URIs
6. Use a production database (PostgreSQL recommended)
7. Configure static files serving
8. Set up proper logging

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review `GOOGLE_OAUTH_SETUP.md`
3. Check django-allauth documentation
4. Review Django documentation

## License

This project uses django-allauth which is licensed under the MIT License.
