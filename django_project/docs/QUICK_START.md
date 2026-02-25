# Quick Start Guide

## ✅ Installation Complete!

All dependencies have been installed and migrations have been applied.

## 🚀 Running the Application

### From PowerShell (Current Directory):

If you're in `django_project/django_project/`, navigate up one level:
```powershell
cd ..
```

Then run:
```powershell
python manage.py runserver
```

### From the Correct Directory:

Make sure you're in the `django_project` folder (where `manage.py` is located):
```powershell
# Check if you're in the right place
dir manage.py

# If you see manage.py, you're good! Run:
python manage.py runserver
```

## 📍 Access the Application

Once the server is running, open your browser and go to:
- **Home Page**: http://localhost:8000/
- **Register**: http://localhost:8000/register/
- **Login**: http://localhost:8000/login/
- **Admin Panel**: http://localhost:8000/admin/

## 👤 Create Admin Account

Before you can use the admin panel, create a superuser:
```powershell
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email
- Password

## 🔐 Role-Based Authentication

The system now has 3 user roles:

1. **Requester** (Default)
   - Create and manage own purchase requests
   - View all PRs

2. **Buyer**
   - All Requester permissions
   - Approve/update any PR
   - Access buyer dashboard

3. **Admin**
   - Full system access
   - Delete PRs
   - Manage all users

## 📝 Testing the Features

### Test Traditional Registration:
1. Go to http://localhost:8000/register/
2. Fill in the form
3. Select a role (Requester, Buyer, or Admin)
4. Click "Create Account"
5. Login with your credentials

### Test Google OAuth (Optional):
1. Follow `GOOGLE_OAUTH_SETUP.md` to configure Google credentials
2. Run `python setup_oauth.py` to set up OAuth
3. Click "Google" button on register/login page
4. Authenticate with Google
5. Select your role

## 🛠️ Common Commands

```powershell
# Run development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Make migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open Python shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

## 📂 Project Structure

```
django_project/
├── manage.py              ← You should be here when running commands
├── db.sqlite3
├── django_project/
│   ├── settings.py
│   └── urls.py
├── users/
│   ├── models.py         ← Profile with role field
│   ├── views.py
│   ├── decorators.py     ← Role-based decorators
│   └── mixins.py         ← Role-based mixins
└── prs/
    ├── models.py
    └── views.py          ← Updated with role permissions
```

## ❓ Troubleshooting

### "No such file or directory: manage.py"
You're in the wrong directory. Navigate to `django_project`:
```powershell
cd "C:\Users\jerem\purches managemnet\Purchase-Request-Management-System\django_project"
```

### "ModuleNotFoundError"
Install missing dependencies:
```powershell
pip install -r requirements.txt
```

### Port already in use
Use a different port:
```powershell
python manage.py runserver 8080
```

### Can't access admin panel
Create a superuser first:
```powershell
python manage.py createsuperuser
```

## 📚 Documentation

- **Full Setup Guide**: `README_ROLE_BASED_AUTH.md`
- **Google OAuth Setup**: `GOOGLE_OAUTH_SETUP.md`
- **Environment Variables**: `.env.example`

## 🎉 You're Ready!

Your PR Management System with role-based authentication and Google OAuth is ready to use!

Start the server and begin testing:
```powershell
python manage.py runserver
```

Then visit: http://localhost:8000/
