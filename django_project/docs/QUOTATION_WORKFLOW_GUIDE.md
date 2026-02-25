# Quotation Workflow Guide

## Overview

The Purchase Request (PR) system now implements a complete quotation workflow where:
1. **Requesters** create PRs with item details (NO price entry)
2. **Buyers** assign vendors to PRs
3. **Vendors** submit price quotations
4. **Buyers** review and approve final prices

This guide explains the complete workflow and how each role interacts with the system.

---

## Workflow Steps

### Step 1: Requester Creates Purchase Request

**Who:** Requester  
**Status:** Open

When creating a new PR, requesters provide:

- **PR Number**: Unique identifier
- **Category**: Select from dropdown (Construction, Consulting, Facility Management, etc.)
- **Item Type**: Automatically populated based on category selection
- **Items Description**: Detailed description of what's needed
- **Quantity**: How many items/units needed
- **Specifications**: Technical specs, dimensions, colors, etc. (optional)
- **Additional Notes**: Any other relevant information (optional)

**Important:** Requesters do NOT enter any price information. The price field is set to €0.00 automatically.

**Dynamic Item Types:**
When you select a category, the Item Type dropdown automatically updates with relevant options:

- **Construction**: Building Materials, Cement & Concrete, Steel & Metal, etc.
- **Consulting**: Business Consulting, IT Consulting, Financial Consulting, etc.
- **Facility Management**: Cleaning Services, Security Services, Maintenance Services, etc.
- **General Goods and Services**: Office Furniture, Stationery, Printing Services, etc.
- **Information Technology**: Computer Hardware, Software, Networking Equipment, etc.
- **Office Supplies**: Paper Products, Writing Instruments, Filing & Storage, etc.

---

### Step 2: Buyer Assigns Vendor

**Who:** Buyer or Admin  
**Status:** Open → Pending

After a PR is created, buyers:

1. Review the PR details
2. Navigate to the PR update page
3. Select an approved vendor from the dropdown
4. Update the status to "Pending"
5. Save the changes

**Vendor Selection:**
- Only approved and active vendors appear in the dropdown
- Vendors are filtered by approval status
- Each vendor shows their name and contact information

---

### Step 3: Vendor Submits Quotation

**Who:** Vendor (assigned to the PR)  
**Status:** Pending

Once assigned, vendors can:

1. View the PR details from their dashboard
2. Review item requirements (type, description, quantity, specifications)
3. Click "Submit Quotation" or "Update Quotation"
4. Enter the following information:
   - **Estimated Price**: Their quoted price for the items
   - **Quotation Notes**: Detailed price breakdown and any notes
   - **Description**: Additional comments (optional)

**Vendor Dashboard:**
- Shows all PRs assigned to the vendor
- Displays pending quotations that need submission
- Tracks approved quotations and total value

**Quotation Information:**
Vendors should include in their quotation notes:
- Itemized price breakdown
- Unit prices
- Delivery costs (if applicable)
- Payment terms
- Validity period of the quotation
- Any conditions or assumptions

---

### Step 4: Buyer Reviews and Approves Quotation

**Who:** Buyer or Admin  
**Status:** Pending → Approval

After vendor submits quotation, buyers:

1. Review the vendor's estimated price and notes
2. Verify the quotation details
3. Navigate to the PR update page
4. Enter the final approved price in the "Approved Price" field
5. Update status to "Approval"
6. Save the changes

**Automatic Tracking:**
When a buyer approves the price:
- `price_approved` is set to `True`
- `price_approved_by` records the buyer's username
- `price_approved_date` records the approval timestamp
- The final price is set in the `total` field

**Buyer Dashboard:**
- Shows all PRs needing attention
- Displays pending quotations for review
- Tracks approved and completed PRs

---

## Role-Based Permissions

### Requester
- **Create PR**: ✅ Can create new PRs with item details
- **Edit PR**: ✅ Can edit their own PRs when status is "Open"
- **View PR**: ✅ Can view their own PRs
- **Delete PR**: ✅ Can delete their own PRs when status is "Open"
- **Price Entry**: ❌ Cannot enter prices
- **Vendor Assignment**: ❌ Cannot assign vendors
- **Quotation**: ❌ Cannot submit quotations

### Vendor
- **Create PR**: ❌ Cannot create PRs
- **Edit PR**: ✅ Can update PRs assigned to them (quotation only)
- **View PR**: ✅ Can view PRs assigned to them
- **Delete PR**: ❌ Cannot delete PRs
- **Price Entry**: ✅ Can submit estimated price (quotation)
- **Vendor Assignment**: ❌ Cannot assign vendors
- **Quotation**: ✅ Can submit and update quotations

### Buyer
- **Create PR**: ❌ Cannot create PRs
- **Edit PR**: ✅ Can update any PR
- **View PR**: ✅ Can view all PRs
- **Delete PR**: ❌ Cannot delete PRs
- **Price Entry**: ✅ Can approve final price
- **Vendor Assignment**: ✅ Can assign vendors
- **Quotation**: ✅ Can review and approve quotations

### Admin
- **Create PR**: ✅ Can create PRs
- **Edit PR**: ✅ Can edit any PR
- **View PR**: ✅ Can view all PRs
- **Delete PR**: ✅ Can delete any PR
- **Price Entry**: ✅ Can enter/modify any price
- **Vendor Assignment**: ✅ Can assign vendors
- **Quotation**: ✅ Full access to quotation workflow

---

## PR Update Form - Field Visibility

The PR update form dynamically shows different fields based on user role:

### Requester View
**Visible Fields:**
- Category
- Item Type (dynamic dropdown)
- Items Description
- Quantity
- Specifications
- Additional Notes

**Hidden Fields:**
- Status
- Vendor
- Estimated Price
- Quotation Notes
- Approved Price
- Payment fields

### Vendor View
**Visible Fields:**
- Estimated Price (required)
- Quotation Notes
- Description

**Hidden Fields:**
- All item detail fields (read-only view)
- Status
- Vendor assignment
- Approved Price
- Payment fields

### Buyer View
**Visible Fields:**
- Status
- Category
- Vendor (dropdown of approved vendors)
- Approved Price (to approve quotation)
- Description
- Payment fields

**Hidden Fields:**
- Item detail fields (requester only)
- Estimated Price (vendor only)
- Quotation Notes (vendor only)

### Admin View
**Visible Fields:**
- All fields (full access)

---

## PR Detail Page - Information Display

The PR detail page shows different sections based on the quotation status:

### Item Details Section
Always visible, shows:
- Item Type
- Quantity
- Items Description
- Specifications

### Quotation Information Section
Visible when:
- Vendor has submitted a quotation, OR
- User is a vendor, buyer, or admin

Shows:
- Estimated Price (vendor's quote)
- Quotation Date
- Submitted By (vendor username)
- Quotation Notes & Breakdown
- Approval Status (if approved)
- Final Approved Price (if approved)

### Price Display Card
Shows different information based on status:
- **No Quotation**: "Pending (Awaiting Quotation)"
- **Quotation Submitted**: "€[estimated_price] (Pending Approval)"
- **Price Approved**: "€[total] (Final Price)"

---

## Status Flow

```
Open → Pending → Approval → Closed
  ↓       ↓         ↓
(Create) (Vendor) (Buyer)
         (Quote)  (Approve)
```

### Status Definitions

1. **Open**: PR created by requester, awaiting buyer action
2. **Pending**: Vendor assigned, awaiting quotation submission
3. **Approval**: Quotation approved, PR can proceed to payment/delivery
4. **On Hold**: Temporarily paused (can be set by buyer/admin)
5. **Closed**: PR completed or cancelled

---

## Dynamic Item Type Dropdown

The system includes an AJAX-powered dynamic dropdown for item types:

### How It Works

1. User selects a category from the dropdown
2. JavaScript detects the change event
3. AJAX request sent to `/api/get-item-types/` with selected category
4. Server returns relevant item types for that category
5. Item Type dropdown is populated with the options
6. User selects the appropriate item type

### Implementation Details

**Backend (views.py):**
```python
def get_item_types(request):
    category = request.GET.get('category', '')
    if category in ITEM_TYPE_CHOICES:
        item_types = [{'value': value, 'label': label} 
                     for value, label in ITEM_TYPE_CHOICES[category]]
        return JsonResponse({'item_types': item_types})
    return JsonResponse({'item_types': []})
```

**Frontend (JavaScript):**
- Listens for category field changes
- Fetches item types via AJAX
- Updates item type dropdown dynamically
- Preserves selected value when editing existing PRs

**URL Configuration:**
```python
path('api/get-item-types/', views.get_item_types, name='get-item-types')
```

---

## Database Fields

### PR Model - Quotation Fields

```python
# Item Details (Requester fills)
item_type = CharField(max_length=200, blank=True)
items_description = TextField(blank=True)
quantity = CharField(max_length=100, blank=True)
specifications = TextField(blank=True)

# Quotation (Vendor fills)
estimated_price = FloatField(null=True, blank=True)
quotation_notes = TextField(blank=True)
quotation_date = DateTimeField(null=True, blank=True)
quotation_submitted_by = ForeignKey(User, ...)

# Approval (Buyer fills)
total = FloatField(default=0.00)  # Final approved price
price_approved = BooleanField(default=False)
price_approved_by = ForeignKey(User, ...)
price_approved_date = DateTimeField(null=True, blank=True)
```

### Helper Method

```python
def has_quotation(self):
    """Check if vendor has submitted quotation"""
    return self.estimated_price is not None and self.estimated_price > 0
```

---

## Best Practices

### For Requesters
1. Provide detailed item descriptions
2. Include all technical specifications
3. Specify exact quantities needed
4. Add any special requirements in notes
5. Don't worry about pricing - vendors will quote

### For Vendors
1. Review all item details carefully
2. Provide itemized price breakdown
3. Include delivery costs if applicable
4. Specify quotation validity period
5. Add any terms and conditions
6. Submit quotations promptly

### For Buyers
1. Assign appropriate vendors based on category
2. Review vendor quotations thoroughly
3. Compare prices if multiple quotes available
4. Verify quotation details before approval
5. Communicate with vendors if clarification needed
6. Update PR status appropriately

### For Admins
1. Monitor the entire workflow
2. Approve vendor registrations promptly
3. Manage vendor ratings and status
4. Handle escalations and issues
5. Maintain system data integrity

---

## Troubleshooting

### Issue: Item Type dropdown is empty
**Solution:** Make sure a category is selected first. The item type dropdown populates based on the selected category.

### Issue: Vendor cannot submit quotation
**Solution:** 
- Verify the vendor is assigned to the PR
- Check that the vendor's account is approved and active
- Ensure the PR status is "Pending"

### Issue: Buyer cannot approve price
**Solution:**
- Verify the vendor has submitted a quotation first
- Check that the buyer has the correct role permissions
- Ensure the estimated_price field has a value

### Issue: Requester cannot edit PR
**Solution:**
- PRs can only be edited by requesters when status is "Open"
- Once a vendor is assigned, requesters cannot modify the PR
- Contact a buyer or admin if changes are needed

---

## API Endpoints

### Get Item Types
**URL:** `/api/get-item-types/`  
**Method:** GET  
**Parameters:** `category` (string)  
**Response:** JSON array of item types

**Example Request:**
```
GET /api/get-item-types/?category=Construction
```

**Example Response:**
```json
{
  "item_types": [
    {"value": "Building Materials", "label": "Building Materials"},
    {"value": "Cement & Concrete", "label": "Cement & Concrete"},
    {"value": "Steel & Metal", "label": "Steel & Metal"},
    ...
  ]
}
```

---

## Summary

The quotation workflow ensures:
- ✅ Clear separation of responsibilities
- ✅ Transparent pricing process
- ✅ Proper approval chain
- ✅ Audit trail for all actions
- ✅ Role-based access control
- ✅ Dynamic form fields based on user role
- ✅ Category-specific item type selection

This workflow promotes accountability, reduces errors, and ensures all stakeholders have the information they need at each stage of the purchase request process.
