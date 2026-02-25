# Quick Test: Multi-Vendor Quotation System

## ✅ Migration Applied Successfully!

The VendorQuotation table has been created. Now you can test the new multi-vendor quotation workflow.

---

## Quick Test Scenario

### Prerequisites
Make sure you have:
- ✅ At least 2-3 vendor accounts (all approved)
- ✅ Vendors registered with same category (e.g., "Construction")
- ✅ One requester account
- ✅ One buyer account

---

## Test Steps

### Step 1: Create Vendors (if not already done)

**Option A: Via Admin Panel**
1. Go to `/admin/`
2. Navigate to Vendors
3. Create 3 vendors:
   - Vendor A: Categories = "Construction"
   - Vendor B: Categories = "Construction"
   - Vendor C: Categories = "Construction, Consulting"
4. Set all to:
   - Status: Active
   - is_approved: True

**Option B: Via Vendor Registration**
1. Create 3 user accounts
2. Each user registers as vendor at `/vendor/register/`
3. Admin approves all vendors at `/vendor/approval/`

---

### Step 2: Requester Creates PR

**Login as Requester**

1. Navigate to dashboard
2. Click "Create New PR"
3. Fill in:
   ```
   PR Number: PR-TEST-MULTI-001
   Category: Construction
   Item Type: Building Materials (auto-populated)
   Items Description: Need 100 bags of cement for construction project
   Quantity: 100 bags
   Specifications: Portland cement, 50kg bags, Grade 42.5
   Additional Notes: Delivery required within 2 weeks
   ```
4. Click "Create Purchase Request"
5. **Verify**: PR created with status "Open", price €0.00

---

### Step 3: Vendors See Available PR

**Login as Vendor A**

1. Go to Vendor Dashboard
2. **Look for**: "Available Purchase Requests" section
3. **Verify**: PR-TEST-MULTI-001 appears in the list
4. **Check**: Shows category, item type, quantity
5. **See**: "Quote" button available

**Repeat for Vendor B and Vendor C**
- All should see the same PR in their dashboard

---

### Step 4: Vendors Submit Quotations

**Vendor A Submits Quote**

1. Login as Vendor A
2. In "Available Purchase Requests", find PR-TEST-MULTI-001
3. Click "Quote" button
4. Fill in:
   ```
   Estimated Price: 5000
   Quotation Notes:
   Price Breakdown:
   - Cement: €45 per bag x 100 = €4,500
   - Delivery: €300
   - Handling: €200
   Total: €5,000
   
   Payment terms: Net 30
   Delivery: 2 weeks
   Warranty: 6 months
   ```
5. Click "Submit Quotation"
6. **Verify**: Success message appears
7. **Check**: PR now appears in "My Orders" section

**Vendor B Submits Quote**

1. Login as Vendor B
2. Click "Quote" on PR-TEST-MULTI-001
3. Fill in:
   ```
   Estimated Price: 4500
   Quotation Notes:
   Price Breakdown:
   - Cement: €42 per bag x 100 = €4,200
   - Delivery: €200
   - Handling: €100
   Total: €4,500
   
   Payment terms: Net 45
   Delivery: 3 weeks
   Warranty: 3 months
   ```
4. Click "Submit Quotation"

**Vendor C Submits Quote**

1. Login as Vendor C
2. Click "Quote" on PR-TEST-MULTI-001
3. Fill in:
   ```
   Estimated Price: 4800
   Quotation Notes:
   Price Breakdown:
   - Cement: €44 per bag x 100 = €4,400
   - Delivery: €250
   - Handling: €150
   Total: €4,800
   
   Payment terms: Net 30
   Delivery: 1 week (FASTEST!)
   Warranty: 12 months
   ```
4. Click "Submit Quotation"

---

### Step 5: Buyer Reviews All Quotations

**Login as Buyer**

1. Go to Buyer Dashboard
2. Find PR-TEST-MULTI-001
3. Click to view PR details
4. Scroll to "Vendor Quotations" section
5. **Verify**: See all 3 quotations displayed:
   ```
   Vendor B - €4,500 (cheapest - shown first)
   Vendor C - €4,800
   Vendor A - €5,000
   ```
6. **Check**: Each quotation shows:
   - Vendor name and rating
   - Estimated price
   - Quotation notes
   - Submission date
   - "Select This Vendor" button

---

### Step 6: Buyer Selects Best Vendor

**Compare Quotations:**
- Vendor B: €4,500 (cheapest, but 3 weeks delivery)
- Vendor C: €4,800 (mid-price, 1 week delivery - FASTEST)
- Vendor A: €5,000 (most expensive)

**Decision: Select Vendor C** (best balance of price and delivery time)

1. Click "Select This Vendor" on Vendor C's quotation
2. Click "Update PR"
3. **Verify**: Form shows Vendor C selected
4. Enter final approved price: `4800`
5. Change status to: `Approval`
6. Update delivery status: `Not Shipped`
7. Click "Approve & Update"
8. **Verify**: Success message appears

---

### Step 7: Verify Results

**Check PR Detail Page:**

1. **Quotations Section** should show:
   - Vendor C's quotation with green background
   - "Selected" badge on Vendor C
   - Other quotations still visible but not selected
   - "Selected by [buyer_username] on [date]"

2. **Price Card** should show:
   - "Final Price: €4,800"
   - Status: "Approval"

3. **Vendor Information** should show:
   - Assigned Vendor: Vendor C
   - Vendor contact info
   - Vendor rating

**Check Vendor C Dashboard:**

1. Login as Vendor C
2. PR-TEST-MULTI-001 should show:
   - Status: Approval
   - Amount: €4,800
   - Green "Approved" badge

**Check Other Vendors:**

1. Login as Vendor A or B
2. PR-TEST-MULTI-001 should:
   - Still appear in "My Orders" (they submitted quotes)
   - Show they were not selected
   - Status shows "Approval" (awarded to another vendor)

---

## Expected Results Summary

### ✅ Requester
- Created PR without entering price
- PR visible to all vendors in category

### ✅ Vendors
- All vendors in "Construction" category saw the PR
- Each vendor submitted their own quotation
- Quotations tracked separately
- Selected vendor gets the order

### ✅ Buyer
- Saw all 3 quotations side-by-side
- Compared prices, terms, and ratings
- Selected best vendor
- Approved final price
- Assigned vendor to PR

### ✅ System
- Multiple quotations stored in VendorQuotation table
- Only one quotation marked as selected
- Complete audit trail maintained
- Status workflow followed correctly

---

## Troubleshooting

### Issue: Vendors don't see PR in "Available Purchase Requests"

**Check:**
- Vendor account is approved (is_approved=True)
- Vendor status is "Active"
- Vendor categories include "Construction"
- PR status is "Open" or "Pending"
- PR is not already assigned to that vendor

**Fix:**
```python
# In Django shell or admin panel
vendor = Vendor.objects.get(name="Vendor A")
vendor.is_approved = True
vendor.status = 'Active'
vendor.categories = 'Construction'
vendor.save()
```

---

### Issue: Quotation not saving

**Check:**
- Vendor is logged in
- Estimated price is entered
- Form validation passes

**Debug:**
Check browser console for JavaScript errors

---

### Issue: Buyer can't see quotations

**Check:**
- Quotations were actually submitted
- Check in admin panel: `/admin/prs/vendorquotation/`
- Verify VendorQuotation records exist

**Query in Django shell:**
```python
from prs.models import PR, VendorQuotation
pr = PR.objects.get(pr_number='PR-TEST-MULTI-001')
quotations = pr.quotations.all()
print(f"Found {quotations.count()} quotations")
for q in quotations:
    print(f"{q.vendor.name}: €{q.estimated_price}")
```

---

### Issue: "Select This Vendor" not working

**Check:**
- User is logged in as buyer
- PR status is not already "Approval"
- Vendor is approved and active

---

## Advanced Testing

### Test Multiple Categories

1. Create PR in "Information Technology"
2. Verify only IT vendors see it
3. Construction vendors should NOT see it

### Test Quotation Updates

1. Vendor submits initial quote: €5,000
2. Vendor updates quote: €4,800
3. Verify only latest quote shows
4. Check VendorQuotation record updated (not duplicated)

### Test Buyer Workflow

1. Create PR
2. Wait for multiple quotations
3. Compare all options
4. Select cheapest vendor
5. Verify selection recorded correctly

---

## Database Verification

### Check VendorQuotation Table

**Via Admin Panel:**
1. Go to `/admin/prs/vendorquotation/`
2. Verify records exist
3. Check fields populated correctly

**Via Django Shell:**
```python
python manage.py shell

from prs.models import VendorQuotation
quotations = VendorQuotation.objects.all()
for q in quotations:
    print(f"PR: {q.pr.pr_number}, Vendor: {q.vendor.name}, Price: €{q.estimated_price}, Selected: {q.is_selected}")
```

---

## Success Criteria

The multi-vendor quotation system is working correctly when:

✅ Multiple vendors can see PRs in their categories  
✅ Each vendor can submit independent quotations  
✅ All quotations are stored separately  
✅ Buyer can see and compare all quotations  
✅ Buyer can select one vendor  
✅ Selected quotation is marked correctly  
✅ Only selected vendor gets the order  
✅ Complete audit trail is maintained  

---

## Next Steps

After successful testing:

1. ✅ Train users on new workflow
2. ✅ Create more test scenarios
3. ✅ Monitor system performance
4. ✅ Gather user feedback
5. ✅ Adjust as needed

---

## Support

For issues or questions:
- Check MULTI_VENDOR_QUOTATION_GUIDE.md for detailed documentation
- Review QUOTATION_WORKFLOW_GUIDE.md for workflow details
- Contact system administrator

---

**Test Date**: _______________  
**Tested By**: _______________  
**Result**: ☐ Pass  ☐ Fail  
**Notes**: _______________________________________________
