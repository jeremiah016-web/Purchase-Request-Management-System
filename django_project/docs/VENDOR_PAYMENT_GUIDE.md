# Vendor Selection and Payment Tracking Guide

## Overview
The Purchase Request Management System now includes vendor selection and payment tracking features. This allows buyers and admins to manage vendor information and track payment status for each purchase request.

## New Fields Added

### Vendor Information
- **Vendor Name**: Name of the vendor/supplier
- **Vendor Contact**: Phone number or email of the vendor

### Payment Information
- **Payment Status**: Current payment status (Pending, Paid, Partially Paid, Cancelled)
- **Payment Date**: Date when payment was made or scheduled
- **Payment Notes**: Additional notes about the payment

## Role-Based Access

### Requester
- **Cannot** see or edit vendor information
- **Cannot** see or edit payment information
- Can only create PRs and edit their own Open PRs (category, description, price)

### Buyer
- **Can** view and edit vendor information
- **Can** view and edit payment information
- **Can** update PR status
- **Can** add approval notes
- **Cannot** edit category or price

### Admin
- **Can** view and edit all fields
- **Can** manage vendor information
- **Can** manage payment information
- **Can** update any PR at any time
- Full control over all purchase requests

## Workflow

### 1. Requester Creates PR
```
1. Requester submits a new PR with:
   - Category
   - Description
   - Price/Total Amount
2. PR status is automatically set to "Open"
3. Vendor and payment fields are empty
```

### 2. Buyer Reviews and Assigns Vendor
```
1. Buyer reviews the PR
2. Buyer adds vendor information:
   - Vendor Name
   - Vendor Contact
3. Buyer can update status to "Pending" or "Approval"
4. Buyer can add approval notes
```

### 3. Buyer/Admin Manages Payment
```
1. After PR is approved, buyer/admin updates:
   - Payment Status (Pending → Paid/Partially Paid)
   - Payment Date
   - Payment Notes
2. Payment status is tracked throughout the process
```

### 4. PR Completion
```
1. Once payment is marked as "Paid"
2. PR can be closed or marked as "Done"
3. All information is preserved for records
```

## How to Use

### For Buyers

#### Assigning a Vendor
1. Go to your Buyer Dashboard
2. Click on a PR that needs vendor assignment
3. Click "Update PR" button
4. Fill in:
   - Vendor Name
   - Vendor Contact
5. Optionally update status
6. Click "Save Changes"

#### Tracking Payment
1. Open the PR detail page
2. Click "Update PR"
3. Update payment information:
   - Payment Status
   - Payment Date (use date picker)
   - Payment Notes
4. Click "Save Changes"

### For Admins

#### Full Management
1. Admins can edit all fields at any time
2. Can override any information
3. Can manage vendor and payment for all PRs
4. Can update status, category, price, vendor, and payment

### For Requesters

#### Viewing Information
1. Requesters can see their PR details
2. **Cannot** see vendor information (unless assigned)
3. **Cannot** see payment information
4. Can only edit their Open PRs

## Payment Status Options

- **Pending**: Payment not yet processed (default)
- **Paid**: Payment completed
- **Partially Paid**: Partial payment made
- **Cancelled**: Payment cancelled

## PR Detail Page

The PR detail page now shows:

### Information Cards
- Status
- Total Amount
- Category
- Payment Status

### Vendor Information Section
- Vendor Name
- Vendor Contact
- (Only visible to buyers and admins)

### Payment Information Section
- Payment Date
- Payment Notes
- (Only visible to buyers and admins)

## Best Practices

### For Buyers
1. **Assign vendors promptly** after reviewing PRs
2. **Keep vendor contact information up to date**
3. **Update payment status** as soon as payment is processed
4. **Add payment notes** for any special circumstances
5. **Use payment date** to track when payments are scheduled

### For Admins
1. **Review vendor assignments** regularly
2. **Monitor payment status** across all PRs
3. **Ensure payment information is accurate**
4. **Use payment notes** for audit trail

### For Requesters
1. **Provide clear descriptions** to help buyers assign appropriate vendors
2. **Include accurate pricing** information
3. **Check PR status** regularly for updates

## Database Fields

```python
# Vendor fields
vendor_name = CharField(max_length=200, blank=True)
vendor_contact = CharField(max_length=100, blank=True)

# Payment fields
payment_status = CharField(choices=['Pending', 'Paid', 'Partially Paid', 'Cancelled'])
payment_date = DateField(null=True, blank=True)
payment_notes = TextField(blank=True)
```

## Migration

The system has been updated with migration `0007_pr_payment_date_pr_payment_notes_pr_payment_status_and_more.py` which adds:
- payment_date
- payment_notes
- payment_status
- vendor_contact
- vendor_name

All existing PRs will have default values:
- payment_status: "Pending"
- Other fields: Empty/blank

## Reporting

### Payment Status Summary
Admins and buyers can track:
- Total PRs by payment status
- Pending payments
- Completed payments
- Payment dates and schedules

### Vendor Summary
- PRs by vendor
- Vendor contact information
- Vendor performance tracking

## Security

- **Role-based access control** ensures only authorized users can edit vendor/payment info
- **Requesters cannot see** sensitive vendor and payment information
- **Audit trail** maintained through payment notes and status updates
- **Date tracking** for all payment activities

## Future Enhancements

Potential future features:
- Vendor database with pre-defined vendors
- Payment approval workflow
- Payment reminders and notifications
- Vendor performance ratings
- Payment history reports
- Integration with accounting systems

## Support

For questions or issues:
1. Check this guide first
2. Review the COMPLETE_SYSTEM_GUIDE.md
3. Contact system administrator
4. Check Django admin panel for detailed information

---

**Last Updated**: February 2026
**Version**: 1.0
