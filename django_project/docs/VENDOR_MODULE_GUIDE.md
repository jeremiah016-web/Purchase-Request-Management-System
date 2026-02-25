# Vendor Module - Complete Guide

## Overview
The Vendor Module is a comprehensive system for managing vendors, tracking communications, processing payments, and monitoring deliveries. This module is accessible to Buyers and Admins only.

## Features

### 1. Vendor Management
- Add, edit, and manage vendor information
- Track vendor status (Active, Inactive, Blacklisted)
- Rate vendors (1-5 stars)
- Store complete business details
- View vendor performance metrics

### 2. Vendor Contact Tracking
- Log all communications with vendors
- Track emails, phone calls, meetings
- Set follow-up reminders
- Link contacts to specific PRs
- View complete communication history

### 3. Payment Processing
- Record payments for purchase requests
- Support multiple payment methods
- Track payment status
- Link payments to vendors and PRs
- Calculate remaining balances automatically

### 4. Delivery Tracking
- Track shipments and deliveries
- Monitor tracking numbers and carriers
- Set expected delivery dates
- Update delivery status
- Identify delayed deliveries

## Access Control

### Buyers
- View all vendors
- Add new vendors
- Edit vendor information
- Log vendor contacts
- Record payments
- Track deliveries
- View vendor performance

### Admins
- All buyer permissions
- Delete vendors
- Full access to all vendor data
- Manage vendor ratings

### Requesters
- Cannot access vendor module
- Cannot see vendor information in PRs
- Cannot see payment details

## How to Use

### Adding a New Vendor

1. Navigate to "Vendors" in the main menu
2. Click "Add Vendor" button
3. Fill in vendor information:
   - **Basic Info**: Name, Contact Person, Email, Phone
   - **Address**: Full business address
   - **Business Details**: Tax ID, Bank Account, Payment Terms
   - **Categories**: Services/products they provide
   - **Status**: Active/Inactive/Blacklisted
4. Click "Save Vendor"

### Viewing Vendor Details

1. Go to Vendors list
2. Click on vendor name or "View" button
3. View comprehensive vendor information:
   - Contact details
   - Business information
   - Performance metrics (Total Orders, Total Value, Rating)
   - Order history
   - Contact history
   - Payment records
   - Delivery tracking

### Contacting a Vendor

1. Open vendor detail page
2. Click "Contact Vendor" button
3. Fill in contact form:
   - Contact Type (Email, Phone, Meeting, Other)
   - Subject
   - Message
   - Response (if received)
   - Follow-up Date (optional)
4. Optionally link to a specific PR
5. Click "Save"

### Recording a Payment

1. From vendor detail page, click "Record Payment"
   OR
2. From PR detail page, add payment
3. Fill in payment details:
   - PR (purchase request)
   - Vendor
   - Amount
   - Payment Method (Bank Transfer, Check, Credit Card, Cash, Other)
   - Payment Date
   - Reference Number
   - Status (Pending, Paid, Partially Paid, Cancelled)
   - Notes
4. Click "Save"

**Note**: Payment status on PR is automatically updated based on total paid amount.

### Tracking Delivery

1. From vendor detail page, click "Track Delivery"
   OR
2. From PR detail page, add delivery tracking
3. Fill in delivery details:
   - PR (purchase request)
   - Vendor
   - Tracking Number
   - Carrier (shipping company)
   - Status (Not Shipped, In Transit, Delivered, Cancelled)
   - Shipped Date
   - Expected Delivery Date
   - Actual Delivery Date
   - Delivery Address
   - Recipient Name and Contact
   - Notes
4. Click "Save"

**Note**: Delivery status on PR is automatically updated.

## Vendor Information Fields

### Basic Information
- **Name**: Vendor/Company name (required, unique)
- **Contact Person**: Primary contact name
- **Email**: Business email
- **Phone**: Business phone number
- **Address**: Full business address
- **Website**: Company website URL

### Business Details
- **Tax ID**: Tax identification or business registration number
- **Bank Account**: Bank account details for payments
- **Payment Terms**: e.g., "Net 30", "Net 60", "COD"
- **Categories**: Comma-separated list of categories they serve

### Status and Performance
- **Status**: Active, Inactive, or Blacklisted
- **Rating**: 0-5 stars (editable by buyers/admins)
- **Total Orders**: Automatically calculated
- **Total Value**: Sum of all PR amounts

### Metadata
- **Date Added**: When vendor was added to system
- **Added By**: User who added the vendor
- **Notes**: Internal notes about the vendor

## Payment Methods

- **Bank Transfer**: Electronic bank-to-bank transfer
- **Check**: Paper check payment
- **Credit Card**: Credit card payment
- **Cash**: Cash payment
- **Other**: Other payment methods

## Payment Status

- **Pending**: Payment not yet processed
- **Paid**: Payment completed
- **Partially Paid**: Partial payment made
- **Cancelled**: Payment cancelled

## Delivery Status

- **Not Shipped**: Item not yet shipped
- **In Transit**: Item is being shipped
- **Delivered**: Item delivered successfully
- **Cancelled**: Delivery cancelled

## Vendor Status

- **Active**: Vendor is active and can receive orders
- **Inactive**: Vendor temporarily inactive
- **Blacklisted**: Vendor blacklisted (cannot receive new orders)

## Workflow Examples

### Example 1: New Purchase Request with Vendor

1. Requester creates PR
2. Buyer reviews and approves PR
3. Buyer assigns vendor from vendor list
4. Buyer contacts vendor (logged in system)
5. Vendor confirms order
6. Buyer records payment
7. Vendor ships item
8. Buyer tracks delivery
9. Item delivered
10. PR marked as complete

### Example 2: Adding New Vendor

1. Buyer needs to order from new supplier
2. Buyer adds new vendor to system
3. Buyer fills in all vendor details
4. Buyer assigns vendor to PR
5. Buyer contacts vendor
6. Vendor relationship established

### Example 3: Payment Tracking

1. PR approved for €1000
2. Buyer records first payment of €500
   - PR payment status: "Partially Paid"
3. Buyer records second payment of €500
   - PR payment status: "Paid"
4. Payment history maintained for audit

## Reports and Analytics

### Vendor Performance
- Total orders per vendor
- Total value per vendor
- Average order value
- Vendor ratings
- On-time delivery rate

### Payment Tracking
- Total payments by vendor
- Payment methods used
- Outstanding balances
- Payment history

### Delivery Tracking
- Delivery status overview
- Delayed deliveries
- Average delivery time
- Carrier performance

## Best Practices

### For Buyers

1. **Keep Vendor Information Updated**
   - Update contact details regularly
   - Maintain accurate business information
   - Update vendor status as needed

2. **Log All Communications**
   - Record every vendor contact
   - Include important details
   - Set follow-up reminders

3. **Track Payments Promptly**
   - Record payments immediately
   - Include reference numbers
   - Add payment notes for clarity

4. **Monitor Deliveries**
   - Update tracking information
   - Check for delays
   - Confirm actual delivery dates

5. **Rate Vendors**
   - Update ratings based on performance
   - Consider quality, timeliness, communication
   - Use ratings for future vendor selection

### For Admins

1. **Review Vendor List Regularly**
   - Remove inactive vendors
   - Update vendor information
   - Monitor vendor performance

2. **Audit Payment Records**
   - Verify payment accuracy
   - Check for discrepancies
   - Maintain payment documentation

3. **Analyze Vendor Performance**
   - Review vendor ratings
   - Identify top performers
   - Address vendor issues

## Integration with PR System

### Automatic Updates
- Assigning vendor to PR updates vendor's order count
- Recording payment updates PR payment status
- Tracking delivery updates PR delivery status

### Linked Information
- Vendors linked to PRs
- Payments linked to vendors and PRs
- Deliveries linked to vendors and PRs
- Contacts can be linked to specific PRs

## Security and Privacy

- Only buyers and admins can access vendor module
- Requesters cannot see vendor information
- Vendor financial details protected
- Audit trail maintained for all actions

## Database Models

### Vendor Model
```python
- name (unique)
- contact_person
- email
- phone
- address
- website
- tax_id
- bank_account
- payment_terms
- categories
- status
- rating
- date_added
- added_by
- notes
```

### VendorContact Model
```python
- vendor (FK)
- pr (FK, optional)
- contact_type
- subject
- message
- response
- contacted_by (FK)
- contact_date
- follow_up_date
```

### Payment Model
```python
- pr (FK)
- vendor (FK)
- amount
- payment_method
- payment_date
- reference_number
- status
- notes
- processed_by (FK)
- created_at
```

### Delivery Model
```python
- pr (FK)
- vendor (FK)
- tracking_number
- carrier
- status
- shipped_date
- expected_delivery_date
- actual_delivery_date
- delivery_address
- recipient_name
- recipient_contact
- notes
- created_by (FK)
- created_at
```

## URLs

- `/vendors/` - Vendor list
- `/vendors/<id>/` - Vendor detail
- `/vendors/new/` - Add vendor
- `/vendors/<id>/update/` - Edit vendor
- `/vendors/<id>/delete/` - Delete vendor (admin only)
- `/vendors/contact/new/` - Log vendor contact
- `/payments/` - Payment list
- `/payments/new/` - Record payment
- `/payments/<id>/update/` - Edit payment
- `/deliveries/` - Delivery list
- `/deliveries/new/` - Track delivery
- `/deliveries/<id>/update/` - Update delivery

## Future Enhancements

Potential future features:
- Vendor performance dashboard
- Automated vendor selection based on ratings
- Vendor comparison tools
- Contract management
- Purchase order generation
- Vendor portal for self-service
- Email integration for automatic contact logging
- SMS notifications for delivery updates
- Vendor payment reminders
- Bulk payment processing
- Advanced reporting and analytics

## Support

For questions or issues:
1. Check this guide
2. Review VENDOR_PAYMENT_GUIDE.md
3. Check COMPLETE_SYSTEM_GUIDE.md
4. Contact system administrator

---

**Last Updated**: February 2026
**Version**: 1.0
