# Multi-Vendor Quotation System Guide

## Overview

The enhanced quotation system allows multiple vendors to submit quotations for the same purchase request. Buyers can then compare all quotations and select the best vendor based on price, rating, and other factors.

---

## How It Works

### 1. Requester Creates PR
- Requester creates a PR with item details (category, item type, description, quantity, specifications)
- NO price is entered by the requester
- PR status is set to "Open"

### 2. Vendors See Available PRs
- All approved vendors can see PRs that match their categories
- Vendors see these PRs in their dashboard under "Available Purchase Requests"
- Vendors can view PR details and submit quotations

### 3. Multiple Vendors Submit Quotations
- Any vendor in the matching category can submit a quotation
- Each vendor provides:
  - Estimated Price
  - Quotation Notes (price breakdown, terms, etc.)
- Vendors can update their quotations before buyer selection
- System tracks all quotations separately

### 4. Buyer Reviews All Quotations
- Buyer sees all submitted quotations on the PR detail page
- Quotations are sorted by price (cheapest first)
- Each quotation shows:
  - Vendor name and rating
  - Estimated price
  - Quotation notes
  - Submission date

### 5. Buyer Selects Best Vendor
- Buyer reviews all quotations
- Buyer selects the best vendor (considering price, rating, terms)
- Buyer approves the final price
- Selected vendor is assigned to the PR
- Status changes to "Approval"

### 6. Delivery and Payment
- Buyer manages delivery status
- Buyer processes payment
- System tracks delivery and payment information

---

## Workflow Diagram

```
┌─────────────────┐
│   Requester     │
│   Creates PR    │
│  (Item Details) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  PR Available to All Vendors        │
│  in Matching Category               │
└────────┬────────────────────────────┘
         │
         ├──────────┬──────────┬──────────┐
         ▼          ▼          ▼          ▼
    ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
    │Vendor A│ │Vendor B│ │Vendor C│ │Vendor D│
    │Submits │ │Submits │ │Submits │ │Submits │
    │Quote   │ │Quote   │ │Quote   │ │Quote   │
    │€5,000  │ │€4,800  │ │€5,200  │ │€4,500  │
    └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘
         │          │          │          │
         └──────────┴──────────┴──────────┘
                    │
                    ▼
         ┌──────────────────┐
         │  Buyer Reviews   │
         │  All Quotations  │
         │  Compares Prices │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Buyer Selects    │
         │ Vendor D         │
         │ (Best Price)     │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Approve Price    │
         │ Assign Vendor    │
         │ Status: Approval │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Delivery &       │
         │ Payment          │
         └──────────────────┘
```

---

## Vendor Categories

Vendors register with specific categories they serve. When a PR is created in a category, all vendors in that category can see it and submit quotations.

### Example Categories:
- Construction
- Consulting
- Facility Management
- General Goods and Services
- Information Technology
- Office Supplies

### Vendor Registration:
When vendors register, they specify their categories (comma-separated):
```
Categories: Construction, Facility Management
```

This vendor will see all PRs in Construction and Facility Management categories.

---

## Vendor Dashboard Features

### Available Purchase Requests Section
Shows PRs that:
- Match vendor's categories
- Are in "Open" or "Pending" status
- Are NOT already assigned to this vendor

For each PR, vendors can:
- View details
- Submit quotation
- Update quotation (before buyer selection)

### My Orders Section
Shows PRs that:
- Are assigned to this vendor
- Vendor has submitted quotation for

---

## Buyer Dashboard Features

### PR Detail Page - Quotations Section
Shows all quotations submitted for the PR:
- Vendor name and rating
- Estimated price (sorted by price)
- Quotation notes
- Submission date
- Selection status

### Buyer Actions:
1. **Review Quotations**: Compare all submitted quotations
2. **Select Vendor**: Click "Select This Vendor" on preferred quotation
3. **Approve Price**: Enter final approved price
4. **Update Status**: Change status to "Approval"
5. **Manage Delivery**: Update delivery status
6. **Process Payment**: Record payment information

---

## Database Structure

### VendorQuotation Model
```python
class VendorQuotation(models.Model):
    pr = ForeignKey(PR)  # The purchase request
    vendor = ForeignKey(Vendor)  # The vendor submitting quotation
    
    estimated_price = FloatField()  # Vendor's quoted price
    quotation_notes = TextField()  # Price breakdown and details
    quotation_date = DateTimeField()  # When submitted
    
    is_selected = BooleanField()  # Selected by buyer
    selected_by = ForeignKey(User)  # Buyer who selected
    selected_date = DateTimeField()  # When selected
    
    class Meta:
        unique_together = ['pr', 'vendor']  # One quote per vendor per PR
        ordering = ['estimated_price']  # Show cheapest first
```

### Relationships:
- One PR can have multiple VendorQuotations
- One Vendor can have multiple VendorQuotations
- Only one VendorQuotation can be selected per PR

---

## Step-by-Step User Guide

### For Vendors

#### Step 1: View Available PRs
1. Login to vendor dashboard
2. Look for "Available Purchase Requests" section
3. See all PRs matching your categories

#### Step 2: Review PR Details
1. Click "View" to see full PR details
2. Review:
   - Item type
   - Description
   - Quantity
   - Specifications
   - Requester notes

#### Step 3: Submit Quotation
1. Click "Quote" button
2. Enter your estimated price
3. Provide detailed quotation notes:
   - Itemized price breakdown
   - Unit prices
   - Delivery costs
   - Payment terms
   - Validity period
4. Click "Submit Quotation"

#### Step 4: Track Status
1. Check "My Orders" section
2. See if your quotation was selected
3. If selected, proceed with delivery

### For Buyers

#### Step 1: Review PR
1. Login to buyer dashboard
2. Find PR needing quotation review
3. Click to view PR details

#### Step 2: Compare Quotations
1. Scroll to "Vendor Quotations" section
2. Review all submitted quotations
3. Compare:
   - Prices (sorted cheapest first)
   - Vendor ratings
   - Quotation notes
   - Payment terms
   - Delivery terms

#### Step 3: Select Vendor
1. Choose the best quotation
2. Consider:
   - Price
   - Vendor rating
   - Past performance
   - Payment terms
   - Delivery timeline
3. Click "Select This Vendor"

#### Step 4: Approve and Assign
1. Click "Update PR"
2. Confirm vendor selection
3. Enter final approved price (or use quoted price)
4. Update status to "Approval"
5. Click "Approve & Update"

#### Step 5: Manage Delivery and Payment
1. Update delivery status as items ship
2. Record payment information
3. Track completion

---

## Benefits of Multi-Vendor Quotation System

### For Requesters
✅ Get competitive pricing  
✅ Multiple vendor options  
✅ Faster response times  
✅ Better quality through competition  

### For Vendors
✅ See all available opportunities  
✅ Compete fairly for business  
✅ No need for buyer assignment first  
✅ Direct access to requirements  

### For Buyers
✅ Compare multiple quotations easily  
✅ Make informed decisions  
✅ Get best value for money  
✅ Transparent selection process  

### For the Organization
✅ Cost savings through competition  
✅ Faster procurement process  
✅ Better vendor relationships  
✅ Complete audit trail  

---

## Example Scenario

### Scenario: Office Furniture Purchase

**1. Requester Creates PR**
- PR Number: PR-2026-001
- Category: General Goods and Services
- Item Type: Office Furniture
- Description: Need 20 office chairs
- Quantity: 20 units
- Specifications: Ergonomic, adjustable height, lumbar support

**2. Vendors See PR**
- Vendor A (Office Supplies) - sees PR
- Vendor B (General Goods) - sees PR
- Vendor C (Office Furniture) - sees PR
- Vendor D (IT Equipment) - does NOT see PR (wrong category)

**3. Vendors Submit Quotations**

**Vendor A:**
- Price: €5,000
- Notes: "Premium ergonomic chairs, 5-year warranty, delivery in 2 weeks"

**Vendor B:**
- Price: €4,500
- Notes: "Quality chairs, 3-year warranty, delivery in 3 weeks"

**Vendor C:**
- Price: €4,800
- Notes: "Ergonomic chairs, 5-year warranty, free delivery, 1 week"

**4. Buyer Reviews**
- Sees 3 quotations
- Compares prices: €4,500, €4,800, €5,000
- Checks ratings: Vendor A (4.5★), Vendor B (4.0★), Vendor C (4.8★)
- Reviews terms: Vendor C has fastest delivery

**5. Buyer Selects**
- Selects Vendor C
- Reason: Good price, highest rating, fastest delivery
- Approves price: €4,800
- Status: Approval

**6. Completion**
- Vendor C delivers chairs in 1 week
- Buyer updates delivery status: Delivered
- Buyer processes payment: €4,800
- PR Status: Closed

---

## Configuration

### Vendor Categories Setup

When vendors register, they specify categories:

```python
# In vendor registration form
categories = "Construction, Facility Management, General Goods and Services"
```

### Matching Logic

```python
# In VendorDashboardView
vendor_categories = [cat.strip() for cat in vendor.categories.split(',')]
available_prs = PR.objects.filter(
    category__in=vendor_categories,
    status__in=['Open', 'Pending']
)
```

---

## Troubleshooting

### Vendor Can't See PRs
**Check:**
- Vendor account is approved
- Vendor status is "Active"
- Vendor categories match PR category
- PR status is "Open" or "Pending"

### Quotation Not Saving
**Check:**
- Vendor is logged in
- Estimated price is entered
- Form validation passes
- No duplicate quotation exists

### Buyer Can't Select Vendor
**Check:**
- Quotations exist for the PR
- PR status is not already "Approval"
- Buyer has correct permissions

---

## API and Technical Details

### Views

**VendorDashboardView:**
- Shows available PRs matching vendor categories
- Shows vendor's assigned PRs
- Filters by approval status

**PRUpdateView:**
- Vendors: Submit/update quotations
- Buyers: Select vendor and approve price
- Creates VendorQuotation records

### Models

**VendorQuotation:**
- Tracks all quotations per PR
- Unique constraint: one quote per vendor per PR
- Ordered by price (cheapest first)

**PR Model:**
- Has many VendorQuotations (pr.quotations.all())
- Has one selected vendor (pr.vendor)
- Tracks approval status

---

## Migration

### Apply Migration
```bash
cd django_project
python manage.py migrate
```

### Migration Details
- Creates VendorQuotation model
- Adds unique constraint
- Sets up relationships

---

## Best Practices

### For Vendors
1. Submit quotations promptly
2. Provide detailed price breakdowns
3. Be competitive but realistic
4. Include all costs (delivery, taxes, etc.)
5. Specify payment terms clearly
6. Update quotations if costs change

### For Buyers
1. Wait for multiple quotations before selecting
2. Consider factors beyond just price
3. Check vendor ratings and history
4. Communicate with vendors if clarification needed
5. Document selection reasoning
6. Update status promptly after selection

### For Admins
1. Approve vendor registrations promptly
2. Verify vendor categories are accurate
3. Monitor quotation activity
4. Handle disputes fairly
5. Maintain vendor ratings

---

## Summary

The multi-vendor quotation system provides:

✅ **Competition**: Multiple vendors compete for each PR  
✅ **Transparency**: All quotations visible to buyers  
✅ **Efficiency**: Vendors see opportunities immediately  
✅ **Savings**: Competition drives better pricing  
✅ **Quality**: Vendor ratings influence selection  
✅ **Audit Trail**: Complete record of all quotations  

This system ensures the best value for the organization while maintaining fair competition among vendors.
