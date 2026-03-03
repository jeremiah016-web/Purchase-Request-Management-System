# Quick Start Guide - Purchase Request Management System

## 🎉 Your System is Ready!

All dependencies are installed and the system is configured. Follow these steps to get started:

---

## Step 1: Run the Server

```bash
cd Purchase-Request-Management-System/django_project
python manage.py runserver
```

Open your browser and go to: **http://localhost:8000**

---

## Step 2: Create Admin Account (if not done)

```bash
python manage.py createsuperuser
```

Enter:
- Username: admin
- Email: admin@example.com
- Password: (your secure password)

---

## Step 3: Access the System

### Admin Panel
- URL: http://localhost:8000/admin
- Login with your superuser credentials
- Manage users, vendors, PRs, payments, etc.

### Main Application
- URL: http://localhost:8000
- Register as a user
- Choose your role: Requester, Buyer, Vendor, or Admin

---

## User Roles & Capabilities

### 👤 Requester
- Create purchase requests
- View own PRs
- Track PR status
- Receive notifications

### 💼 Buyer
- Review all PRs
- Assign vendors
- Approve quotations
- Process payments
- Manage deliveries

### 🏢 Vendor
- View available PRs
- Submit quotations
- Update delivery status
- Receive payment notifications

### 👨‍💼 Admin
- Full system access
- Manage all users
- Approve vendors
- Override any action
- View system statistics

---

## Quick Workflow Example

### 1. Create a Purchase Request (Requester)

1. Login as requester
2. Click "New PR"
3. Fill in details:
   - PR Number: PR-2024-001
   - Category: Information Technology
   - Item Type: Laptop
   - Description: Dell XPS 15
   - Quantity: 5 units
4. Submit

### 2. Submit Quotation (Vendor)

1. Login as vendor
2. View available PRs
3. Click on PR-2024-001
4. Click "Update" or "Submit Quotation"
5. Enter:
   - Estimated Price: $7,500
   - Quotation Notes: 5x Dell XPS @ $1,500 each
6. Submit

### 3. Approve & Process (Buyer)

1. Login as buyer
2. View pending PRs
3. Click on PR-2024-001
4. Review quotation
5. Select vendor
6. Approve price
7. Process payment
8. Track delivery

---

## New Features Available

### 💳 Payment Gateway Integration

**Test Stripe Payment:**
```python
from prs.payment_gateway import StripePaymentGateway

result = StripePaymentGateway.create_payment_intent(
    amount=100.00,
    metadata={'pr_number': 'PR-2024-001'}
)
```

**Test PayPal Payment:**
```python
from prs.payment_gateway import PayPalPaymentGateway

result = PayPalPaymentGateway.create_payment(
    amount=100.00,
    description='Test payment'
)
```

### 📦 Delivery Tracking

**Track Shipment:**
```python
from prs.delivery_tracking import track_shipment

tracking = track_shipment(
    tracking_number='1234567890',
    carrier='fedex'
)
```

### 📧 Email Notifications

**Send Notification:**
```python
from prs.notifications import send_pr_created_notification

send_pr_created_notification(pr)
```

### ✅ Payment Approval Workflow

**Request Approval:**
```python
from prs.approval_workflow import request_payment_approval

approval = request_payment_approval(
    pr=pr,
    amount=5000.00,
    requested_by=buyer
)
```

### 📄 Invoice Generation

**Generate Invoice:**
```python
from prs.invoice_generator import generate_invoice

invoice_path = generate_invoice(payment, pr)
```

---

## Configuration (Optional)

### Enable Payment Gateways

Edit `django_project/.env`:

```env
# Stripe (Get keys from https://dashboard.stripe.com)
STRIPE_PUBLIC_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key

# PayPal (Get keys from https://developer.paypal.com)
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
```

### Enable Email Notifications

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SITE_URL=http://localhost:8000
```

### Enable Delivery Tracking

```env
FEDEX_API_KEY=your_key
UPS_API_KEY=your_key
DHL_API_KEY=your_key
USPS_API_KEY=your_key
```

---

## Testing Without API Keys

All features work with mock/test data even without API keys:

- **Payments**: Use test mode
- **Tracking**: Returns mock tracking data
- **Emails**: Use console backend (prints to terminal)
- **Invoices**: Generate PDFs locally

---

## Common Tasks

### Create Test Users

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from users.models import Profile

# Create requester
user1 = User.objects.create_user('john_requester', 'john@example.com', 'password123')
user1.profile.role = 'requester'
user1.profile.save()

# Create buyer
user2 = User.objects.create_user('jane_buyer', 'jane@example.com', 'password123')
user2.profile.role = 'buyer'
user2.profile.save()

# Create vendor
user3 = User.objects.create_user('vendor1', 'vendor@example.com', 'password123')
user3.profile.role = 'vendor'
user3.profile.save()
```

### Create Test Vendor

```python
from prs.models import Vendor

vendor = Vendor.objects.create(
    name='Tech Solutions Inc',
    contact_person='John Doe',
    email='vendor@techsolutions.com',
    phone='555-1234',
    categories='Information Technology',
    status='Active',
    is_approved=True
)
```

### View All PRs

```python
from prs.models import PR

prs = PR.objects.all()
for pr in prs:
    print(f"{pr.pr_number} - {pr.status} - ${pr.total}")
```

---

## Documentation

📖 **Complete Guides:**
- `INSTALLATION.md` - Installation instructions
- `PAYMENT_TRACKING_GUIDE.md` - Payment & tracking features
- `UML_DIAGRAMS.md` - System architecture diagrams
- `docs/WORKFLOW_GUIDE.md` - Workflow documentation

---

## Troubleshooting

### Server won't start
```bash
# Check for errors
python manage.py check

# Try different port
python manage.py runserver 8080
```

### Can't login
```bash
# Reset password
python manage.py changepassword username
```

### Database issues
```bash
# Reset database (WARNING: deletes all data)
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## Next Steps

1. ✅ System is running
2. 👥 Create user accounts
3. 🏢 Add vendors
4. 📝 Create your first PR
5. 💳 Configure payment gateways (optional)
6. 📧 Set up email notifications (optional)
7. 🚀 Deploy to production

---

## Support & Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Stripe Docs**: https://stripe.com/docs
- **PayPal Docs**: https://developer.paypal.com/docs/

---

**Happy Managing! 🎉**

Your Purchase Request Management System is ready to use with all enterprise features enabled!
