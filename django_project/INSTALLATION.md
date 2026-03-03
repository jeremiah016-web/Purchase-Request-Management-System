# Installation Guide

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

## Quick Installation

### Step 1: Navigate to Project Directory

```bash
cd Purchase-Request-Management-System/django_project
```

### Step 2: Install Dependencies

All required packages are already installed! ✅

If you need to reinstall:

```bash
pip install Django django-crispy-forms crispy-bootstrap4 django-allauth
pip install stripe paypalrestsdk requests python-dotenv python-decouple reportlab
```

### Step 3: Configure Environment Variables

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env with your settings (use notepad or any text editor)
notepad .env
```

### Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 6: Run the Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

## What's Installed

✅ Django 6.0.2 - Web framework
✅ django-crispy-forms - Form styling
✅ crispy-bootstrap4 - Bootstrap 4 support
✅ django-allauth - Authentication
✅ Pillow 12.1.1 - Image processing
✅ stripe - Payment gateway
✅ paypalrestsdk - PayPal integration
✅ reportlab - PDF generation
✅ requests - HTTP library
✅ python-dotenv - Environment variables
✅ python-decouple - Configuration management

## Optional Features

### Email Notifications

For email notifications, configure in `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Payment Gateways

Get your API keys:

**Stripe**: https://dashboard.stripe.com/register
**PayPal**: https://developer.paypal.com/

Add to `.env`:

```env
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
```

### Delivery Tracking

Add carrier API keys to `.env`:

```env
FEDEX_API_KEY=your_key
UPS_API_KEY=your_key
DHL_API_KEY=your_key
USPS_API_KEY=your_key
```

## Troubleshooting

### Issue: Module not found

**Solution**: Reinstall the package
```bash
pip install <package-name>
```

### Issue: Database errors

**Solution**: Delete db.sqlite3 and run migrations again
```bash
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Port already in use

**Solution**: Use a different port
```bash
python manage.py runserver 8080
```

## Next Steps

1. ✅ Installation complete
2. 📖 Read `PAYMENT_TRACKING_GUIDE.md` for feature documentation
3. 🎨 Customize templates in `prs/templates/`
4. 🔧 Configure settings in `django_project/settings.py`
5. 🚀 Deploy to production (Heroku, Railway, etc.)

## Support

For issues:
- Check Django logs
- Review `.env` configuration
- Test with mock/sandbox data first
- Contact system administrator

**Installation successful!** 🎉
