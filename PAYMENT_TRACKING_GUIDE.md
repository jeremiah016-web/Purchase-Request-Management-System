# Payment & Tracking System - Complete Guide

## Overview

This guide covers all the enhanced features added to your Purchase Request Management System:

1. **Payment Gateway Integration** (Stripe & PayPal)
2. **Real-time Delivery Tracking** (FedEx, UPS, DHL, USPS)
3. **Email Notifications** (Automated alerts)
4. **Payment Approval Workflow** (Multi-level approval)
5. **Invoice Generation** (PDF invoices)

---

## 1. Payment Gateway Integration

### Supported Payment Methods

- **Stripe**: Credit/Debit cards, digital wallets
- **PayPal**: PayPal accounts, credit cards
- **Traditional**: Bank transfer, check, cash

### Setup Instructions

#### Step 1: Install Dependencies

```bash
cd django_project
pip install -r requirements.txt
```

#### Step 2: Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Stripe Configuration
STRIPE_PUBLIC_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_secret_here

# PayPal Configuration
PAYPAL_MODE=sandbox  # or 'live' for production
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
```

#### Step 3: Get API Keys

**Stripe:**
1. Go to https://dashboard.stripe.com/register
2. Create an account
3. Navigate to Developers → API keys
4. Copy your publishable and secret keys

**PayPal:**
1. Go to https://developer.paypal.com/
2. Create an app
3. Get your Client ID and Secret

### Usage Examples

#### Process Stripe Payment

```python
from prs.payment_gateway import StripePaymentGateway

# Create payment intent
result = StripePaymentGateway.create_payment_intent(
    amount=1000.00,  # Amount in dollars
    currency='usd',
    metadata={'pr_number': 'PR-2024-001'}
)

if result['success']:
    client_secret = result['client_secret']
    # Use client_secret in frontend to complete payment
```

#### Process PayPal Payment

```python
from prs.payment_gateway import PayPalPaymentGateway

# Create payment
result = PayPalPaymentGateway.create_payment(
    amount=1000.00,
    currency='USD',
    description='Payment for PR-2024-001'
)

if result['success']:
    approval_url = result['approval_url']
    # Redirect user to approval_url
```

---

## 2. Delivery Tracking System

### Supported Carriers

- FedEx
- UPS
- DHL
- USPS

### Setup Instructions

#### Configure API Keys

Add carrier API keys to `.env`:

```env
FEDEX_API_KEY=your_fedex_key
UPS_API_KEY=your_ups_key
DHL_API_KEY=your_dhl_key
USPS_API_KEY=your_usps_key
```

### Usage Examples

#### Track a Shipment

```python
from prs.delivery_tracking import track_shipment

# Track shipment
tracking_info = track_shipment(
    tracking_number='1234567890',
    carrier='fedex'
)

print(tracking_info)
# Output:
# {
#     'success': True,
#     'carrier': 'FedEx',
#     'tracking_number': '1234567890',
#     'status': 'In Transit',
#     'location': 'Distribution Center',
#     'estimated_delivery': '2024-12-25',
#     'events': [...]
# }
```

#### Update Delivery Status

```python
from prs.models import Delivery

delivery = Delivery.objects.get(id=1)

# Get real-time tracking
tracking_info = track_shipment(
    tracking_number=delivery.tracking_number,
    carrier=delivery.carrier
)

# Update delivery status
if tracking_info['success']:
    delivery.status = tracking_info['status']
    delivery.save()
```

---

## 3. Email Notification System

### Notification Types

1. **PR Created** - Sent to requester
2. **Status Changed** - Sent to relevant parties
3. **Quotation Submitted** - Sent to buyers
4. **Vendor Selected** - Sent to vendor and requester
5. **Payment Processed** - Sent to all parties
6. **Shipment Update** - Sent to requester
7. **Delivery Completed** - Sent to requester
8. **Payment Approval Required** - Sent to approvers

### Setup Instructions

#### Configure Email Settings

Add to `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SITE_URL=http://localhost:8000
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the app password in EMAIL_HOST_PASSWORD

### Usage Examples

#### Send PR Created Notification

```python
from prs.notifications import send_pr_created_notification

# Automatically send when PR is created
send_pr_created_notification(pr)
```

#### Send Payment Notification

```python
from prs.notifications import send_payment_notification

# Send payment notification
send_payment_notification(
    payment=payment,
    pr=pr,
    recipients=[buyer, requester, vendor.user]
)
```

#### Send Shipment Update

```python
from prs.notifications import send_shipment_notification

# Send shipment update
send_shipment_notification(
    delivery=delivery,
    pr=pr,
    recipients=[pr.author]
)
```

---

## 4. Payment Approval Workflow

### Approval Levels

Define approval levels based on payment amounts:

- **Level 1**: $0 - $1,000 (Manager approval)
- **Level 2**: $1,000 - $10,000 (Director approval)
- **Level 3**: $10,000+ (CFO approval)

### Setup Instructions

#### Create Approval Levels

```python
from prs.approval_workflow import ApprovalLevel
from django.contrib.auth.models import User

# Get approvers
manager = User.objects.get(username='manager')
director = User.objects.get(username='director')
cfo = User.objects.get(username='cfo')

# Create Level 1
level1 = ApprovalLevel.objects.create(
    name='Manager Approval',
    min_amount=0,
    max_amount=1000,
    order=1
)
level1.approvers.add(manager)

# Create Level 2
level2 = ApprovalLevel.objects.create(
    name='Director Approval',
    min_amount=1000,
    max_amount=10000,
    order=2
)
level2.approvers.add(director)

# Create Level 3
level3 = ApprovalLevel.objects.create(
    name='CFO Approval',
    min_amount=10000,
    max_amount=None,  # Unlimited
    order=3
)
level3.approvers.add(cfo)
```

### Usage Examples

#### Request Payment Approval

```python
from prs.approval_workflow import request_payment_approval

# Request approval for payment
approval = request_payment_approval(
    pr=pr,
    amount=5000.00,
    requested_by=buyer,
    notes='Urgent purchase request'
)
```

#### Approve Payment

```python
from prs.approval_workflow import approve_payment

# Approve a payment step
success = approve_payment(
    approval_id=approval.id,
    level_id=level.id,
    approver=director,
    comments='Approved - within budget'
)
```

#### Check Approval Status

```python
# Check if fully approved
if approval.is_fully_approved():
    # Process payment
    payment = Payment.objects.create(
        pr=pr,
        amount=approval.amount,
        payment_method='Bank Transfer',
        payment_date=timezone.now().date(),
        status='Paid',
        processed_by=buyer
    )
```

#### Get Pending Approvals

```python
from prs.approval_workflow import get_my_pending_approvals

# Get approvals pending for current user
pending = get_my_pending_approvals(request.user)

for step in pending:
    print(f"PR: {step.payment_approval.pr.pr_number}")
    print(f"Amount: ${step.payment_approval.amount}")
    print(f"Level: {step.approval_level.name}")
```

---

## 5. Invoice Generation

### Features

- Professional PDF invoices
- Company branding
- Itemized billing
- Payment details
- Automatic generation

### Usage Examples

#### Generate Invoice

```python
from prs.invoice_generator import generate_invoice

# Generate invoice for payment
invoice_path = generate_invoice(
    payment=payment,
    pr=pr
)

print(f"Invoice generated: {invoice_path}")
# Output: /media/invoices/invoice_PR-2024-001_1.pdf
```

#### Custom Invoice Path

```python
# Generate with custom path
invoice_path = generate_invoice(
    payment=payment,
    pr=pr,
    output_path='/custom/path/invoice.pdf'
)
```

#### Send Invoice via Email

```python
from django.core.mail import EmailMessage

# Generate invoice
invoice_path = generate_invoice(payment, pr)

# Send via email
email = EmailMessage(
    subject=f'Invoice for {pr.pr_number}',
    body='Please find attached your invoice.',
    from_email=settings.EMAIL_HOST_USER,
    to=[pr.author.email]
)
email.attach_file(invoice_path)
email.send()
```

---

## Complete Workflow Example

Here's a complete workflow from PR creation to delivery:

```python
from django.contrib.auth.models import User
from prs.models import PR, Vendor, Payment, Delivery
from prs.notifications import *
from prs.approval_workflow import *
from prs.payment_gateway import process_payment
from prs.delivery_tracking import track_shipment
from prs.invoice_generator import generate_invoice

# 1. Requester creates PR
requester = User.objects.get(username='john_requester')
pr = PR.objects.create(
    pr_number='PR-2024-001',
    category='Information Technology',
    item_type='Laptop',
    items_description='Dell XPS 15, 16GB RAM, 512GB SSD',
    quantity='5 units',
    author=requester,
    status='Open'
)

# Send notification
send_pr_created_notification(pr)

# 2. Buyer reviews and assigns vendor
buyer = User.objects.get(username='jane_buyer')
vendor = Vendor.objects.get(name='Tech Solutions')

pr.status = 'Pending'
pr.vendor = vendor
pr.save()

# 3. Vendor submits quotation
pr.estimated_price = 7500.00
pr.quotation_notes = '5x Dell XPS 15 @ $1,500 each'
pr.save()

# Notify buyer
send_quotation_notification(pr, vendor, [buyer])

# 4. Buyer approves price
pr.total = 7500.00
pr.price_approved = True
pr.status = 'Approval'
pr.save()

# Notify vendor and requester
send_vendor_selected_notification(pr)

# 5. Request payment approval
approval = request_payment_approval(
    pr=pr,
    amount=7500.00,
    requested_by=buyer,
    notes='Approved vendor quotation'
)

# Notify approvers
from prs.notifications import send_payment_approval_notification
approvers = approval.get_pending_approvers()
send_payment_approval_notification(pr, approvers)

# 6. Director approves
director = User.objects.get(username='director')
approve_payment(
    approval_id=approval.id,
    level_id=2,  # Director level
    approver=director,
    comments='Approved'
)

# 7. Process payment (after full approval)
if approval.is_fully_approved():
    # Option A: Traditional payment
    payment = Payment.objects.create(
        pr=pr,
        vendor=vendor,
        amount=7500.00,
        payment_method='Bank Transfer',
        payment_date=timezone.now().date(),
        reference_number='TXN-123456',
        status='Paid',
        processed_by=buyer
    )
    
    # Option B: Online payment (Stripe)
    result = process_payment(
        payment_method='stripe',
        amount=7500.00,
        pr_number=pr.pr_number
    )
    
    # Generate invoice
    invoice_path = generate_invoice(payment, pr)
    
    # Send payment notification
    send_payment_notification(payment, pr, [requester, vendor.user])

# 8. Vendor ships items
delivery = Delivery.objects.create(
    pr=pr,
    vendor=vendor,
    tracking_number='1234567890',
    carrier='FedEx',
    status='In Transit',
    shipped_date=timezone.now().date(),
    expected_delivery_date='2024-12-25',
    delivery_address='123 Main St, City, State',
    recipient_name=requester.get_full_name(),
    created_by=vendor.user
)

# Send shipment notification
send_shipment_notification(delivery, pr, [requester])

# 9. Track delivery
tracking_info = track_shipment(
    tracking_number=delivery.tracking_number,
    carrier=delivery.carrier
)

# Update delivery status
delivery.status = tracking_info['status']
delivery.save()

# 10. Delivery completed
delivery.status = 'Delivered'
delivery.actual_delivery_date = timezone.now().date()
delivery.save()

# Send completion notification
send_delivery_completed_notification(delivery, pr)

# Close PR
pr.status = 'Closed'
pr.save()
```

---

## Testing

### Test Payment Gateway (Sandbox Mode)

```python
# Test Stripe payment
from prs.payment_gateway import StripePaymentGateway

result = StripePaymentGateway.create_payment_intent(
    amount=100.00,
    metadata={'test': 'true'}
)

print(result)
```

### Test Delivery Tracking (Mock Data)

```python
# Without API keys, system returns mock data
from prs.delivery_tracking import track_shipment

tracking = track_shipment('TEST123', 'fedex')
print(tracking)
```

### Test Email Notifications (Console Backend)

For testing, use console email backend in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## Troubleshooting

### Payment Gateway Issues

**Problem**: Stripe/PayPal not working
**Solution**: 
- Check API keys in `.env`
- Verify sandbox/live mode
- Check internet connection
- Review logs for errors

### Email Not Sending

**Problem**: Emails not being sent
**Solution**:
- Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- For Gmail, use App Password
- Check SMTP settings
- Test with console backend first

### Tracking Not Working

**Problem**: Delivery tracking returns errors
**Solution**:
- Verify carrier API keys
- Check tracking number format
- System falls back to mock data if APIs unavailable

---

## Security Best Practices

1. **Never commit `.env` file** - Keep credentials secret
2. **Use environment variables** - Don't hardcode API keys
3. **Enable HTTPS** - For production deployments
4. **Validate payment amounts** - Prevent manipulation
5. **Log all transactions** - Maintain audit trail
6. **Implement rate limiting** - Prevent abuse
7. **Use webhook signatures** - Verify payment callbacks

---

## Next Steps

1. **Run migrations** to add approval workflow models
2. **Configure environment variables** with your API keys
3. **Set up approval levels** for your organization
4. **Test payment gateways** in sandbox mode
5. **Configure email settings** for notifications
6. **Train users** on the new features

---

## Support

For issues or questions:
- Check logs in `django_project/logs/`
- Review Django admin for data
- Test with mock/sandbox data first
- Contact system administrator

---

**Congratulations!** Your Purchase Request Management System now has enterprise-grade payment and tracking capabilities! 🎉
