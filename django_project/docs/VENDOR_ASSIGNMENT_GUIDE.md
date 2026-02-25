# Vendor Assignment Guide

## Overview
This guide explains how to assign vendors to Purchase Requests (PRs) in the system.

## Who Can Assign Vendors?

### Buyers
- Can assign approved vendors to any PR
- Can view all approved vendors
- Cannot edit vendor details

### Admins
- Can assign vendors to any PR
- Can create and edit vendors
- Can approve/reject vendor registrations
- Full control over vendor management

### Requesters
- Cannot assign vendors
- Cannot see vendor information

### Vendors
- Cannot assign themselves
- Can only view PRs assigned to them

## How to Assign a Vendor to a PR

### Method 1: From PR Detail Page

1. **Navigate to the PR**
   - Go to your dashboard
   - Click on the PR you want to assign a vendor to

2. **Click "Update PR" or "Edit PR"**
   - Button is visible to buyers and admins
   - Opens the PR update form

3. **Select Vendor from Dropdown**
   - Look for "Assign Vendor" field
   - Dropdown shows only approved and active vendors
   - Select the appropriate vendor

4. **Save Changes**
   - Click "Save Changes" button
   - Vendor is now assigned to the PR

### Method 2: From Buyer Dashboard

1. **Go to Buyer Dashboard**
   - Click "Dashboard" in navigation

2. **Find the PR in the list**
   - Browse through pending PRs

3. **Click "Update" button**
   - Opens PR update form

4. **Assign Vendor**
   - Select vendor from dropdown
   - Update status if needed
   - Save changes

### Method 3: From Vendor Detail Page

1. **Go to Vendors List**
   - Click "Vendors" in navigation

2. **Select a Vendor**
   - Click on vendor name or "View" button

3. **View Vendor's Orders**
   - See all PRs assigned to this vendor
   - Click on any PR to view details

4. **Assign More PRs**
   - Go back to PR list
   - Update PRs to assign to this vendor

## Vendor Selection Criteria

When assigning vendors, consider:

### 1. Vendor Status
- Only **Active** and **Approved** vendors appear in dropdown
- Pending vendors are not available
- Inactive vendors are not available
- Blacklisted vendors are not available

### 2. Vendor Rating
- Check vendor rating (1-5 stars)
- Higher rated vendors may provide better service
- Rating visible on vendor detail page

### 3. Vendor Categories
- Check if vendor serves the PR category
- Categories listed on vendor profile
- Match PR category with vendor expertise

### 4. Payment Terms
- Review vendor payment terms
- Consider: Net 30, Net 60, COD, etc.
- Ensure terms align with company policy

### 5. Past Performance
- Check vendor's order history
- Review total orders and total value
- Look at delivery and payment records

## Vendor Assignment Workflow

### Standard Workflow

```
1. Requester creates PR
   ↓
2. PR status: "Open"
   ↓
3. Buyer reviews PR
   ↓
4. Buyer assigns vendor
   ↓
5. Buyer updates status to "Pending" or "Approval"
   ↓
6. Vendor sees PR in their dashboard
   ↓
7. Vendor fulfills order
   ↓
8. Buyer tracks payment and delivery
   ↓
9. PR marked as "Done"
```

### Quick Assignment Workflow

```
1. Buyer opens PR
   ↓
2. Click "Update PR"
   ↓
3. Select vendor from dropdown
   ↓
4. Change status to "Pending"
   ↓
5. Add notes in description
   ↓
6. Save changes
```

## What Happens After Assignment?

### For the Vendor
- PR appears in vendor's dashboard
- Vendor can view PR details
- Vendor sees payment and delivery information
- Vendor receives order notification (if configured)

### For the Buyer
- Can track vendor performance
- Can record payments
- Can track deliveries
- Can contact vendor through system

### For the Requester
- Cannot see which vendor is assigned (for privacy)
- Can see PR status updates
- Can track PR progress

### For the Admin
- Full visibility of all assignments
- Can reassign vendors if needed
- Can monitor vendor performance
- Can manage vendor relationships

## Reassigning Vendors

### When to Reassign
- Vendor cannot fulfill order
- Vendor is unresponsive
- Better vendor becomes available
- Vendor requests to be removed

### How to Reassign
1. Open the PR
2. Click "Update PR"
3. Select different vendor from dropdown
4. Add note explaining reassignment
5. Save changes

### Best Practices
- Notify original vendor of reassignment
- Document reason for change
- Update PR status if needed
- Inform requester of any delays

## Bulk Assignment (Future Feature)

Currently, vendors must be assigned one PR at a time. Future enhancements may include:
- Bulk vendor assignment
- Auto-assignment based on category
- Vendor rotation system
- Load balancing across vendors

## Vendor Assignment Reports

### Available Information
- Total PRs per vendor
- Total value per vendor
- Average order value
- Vendor utilization rate
- Pending vs completed orders

### How to View
1. Go to Vendor Detail page
2. View statistics cards
3. Check "Orders" tab
4. Review payment and delivery tabs

## Troubleshooting

### Vendor Not Appearing in Dropdown

**Possible Reasons:**
- Vendor not approved yet
- Vendor status is "Inactive" or "Blacklisted"
- Vendor status is "Pending"
- No vendors registered in system

**Solution:**
- Check vendor status in Vendors list
- Contact admin to approve vendor
- Ensure vendor has completed registration

### Cannot Assign Vendor

**Possible Reasons:**
- User is not a buyer or admin
- PR is in wrong status
- Form permissions issue

**Solution:**
- Verify user role
- Check PR status
- Contact system administrator

### Vendor Assignment Not Saving

**Possible Reasons:**
- Form validation error
- Database connection issue
- Permission issue

**Solution:**
- Check for error messages
- Verify all required fields
- Try refreshing page
- Contact system administrator

## Best Practices

### For Buyers

1. **Review Vendor Before Assignment**
   - Check vendor rating
   - Review past performance
   - Verify vendor categories

2. **Add Assignment Notes**
   - Document why vendor was chosen
   - Include any special instructions
   - Note expected delivery date

3. **Update PR Status**
   - Change status to "Pending" after assignment
   - Update to "Approval" when vendor confirms
   - Keep status current

4. **Monitor Vendor Performance**
   - Track delivery times
   - Record payment status
   - Update vendor ratings

5. **Communicate with Vendors**
   - Log all communications
   - Set follow-up reminders
   - Keep records updated

### For Admins

1. **Maintain Vendor Database**
   - Keep vendor information current
   - Remove inactive vendors
   - Update vendor ratings

2. **Approve Vendors Promptly**
   - Review registrations regularly
   - Verify vendor credentials
   - Approve qualified vendors quickly

3. **Monitor Assignment Patterns**
   - Track which vendors get most orders
   - Identify underutilized vendors
   - Balance workload across vendors

4. **Handle Vendor Issues**
   - Address vendor complaints
   - Resolve assignment conflicts
   - Update vendor status as needed

## Quick Reference

### Assign Vendor to PR
```
Dashboard → Select PR → Update PR → Assign Vendor → Save
```

### View Vendor's Orders
```
Vendors → Select Vendor → Orders Tab
```

### Check Vendor Status
```
Vendors → Search/Filter → View Status Column
```

### Reassign Vendor
```
PR Detail → Update PR → Change Vendor → Save
```

### View Assignment History
```
Vendor Detail → Orders Tab → View All PRs
```

## Related Documentation

- [Vendor Module Guide](VENDOR_MODULE_GUIDE.md) - Complete vendor management
- [Vendor Payment Guide](VENDOR_PAYMENT_GUIDE.md) - Payment tracking
- [Buyer Approval Guide](BUYER_APPROVAL_GUIDE.md) - PR approval workflow
- [Complete System Guide](COMPLETE_SYSTEM_GUIDE.md) - Full system overview

## Support

For questions or issues with vendor assignment:
1. Check this guide
2. Review vendor status
3. Verify user permissions
4. Contact system administrator

---

**Last Updated**: February 2026
**Version**: 1.0
