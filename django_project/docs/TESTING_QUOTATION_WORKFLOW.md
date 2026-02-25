# Testing the Quotation Workflow

## Quick Test Guide

This guide helps you test the complete quotation workflow from start to finish.

---

## Prerequisites

Before testing, ensure you have:

1. ✅ At least one user account for each role:
   - Requester
   - Buyer
   - Vendor (with approved vendor profile)
   - Admin

2. ✅ At least one approved vendor in the system
3. ✅ Django server running: `python manage.py runserver`

---

## Test Scenario: Complete Purchase Request Flow

### Test 1: Requester Creates PR

**Login as:** Requester

**Steps:**
1. Navigate to dashboard (should see Requester Dashboard)
2. Click "Create New PR" or navigate to `/pr/new/`
3. Fill in the form:
   - PR Number: `PR-TEST-001`
   - Category: Select `Construction`
   - Item Type: Should auto-populate with construction options - select `Building Materials`
   - Items Description: `Need 100 bags of cement for building project`
   - Quantity: `100 bags`
   - Specifications: `Portland cement, 50kg bags, Grade 42.5`
   - Additional Notes: `Delivery required to site address`
4. Click "Create Purchase Request"

**Expected Results:**
- ✅ PR created successfully
- ✅ Status is "Open"
- ✅ Total price is €0.00
- ✅ No vendor assigned
- ✅ Item type dropdown populated based on category selection
- ✅ Redirected to PR detail page

**Verify:**
- PR appears in requester's dashboard
- All item details are saved correctly
- Item type matches the selected value

---

### Test 2: Buyer Assigns Vendor

**Login as:** Buyer

**Steps:**
1. Navigate to Buyer Dashboard
2. Find `PR-TEST-001` in the list
3. Click on the PR to view details
4. Click "Update PR"
5. In the update form:
   - Vendor: Select an approved vendor from dropdown
   - Status: Change to `Pending`
6. Click "Approve & Update"

**Expected Results:**
- ✅ Vendor assigned successfully
- ✅ Status changed to "Pending"
- ✅ Only approved, active vendors appear in dropdown
- ✅ Item detail fields are not visible (requester only)
- ✅ Quotation fields are not visible (vendor only)

**Verify:**
- PR detail page shows assigned vendor information
- Vendor name, contact, rating, and payment terms displayed
- PR appears in vendor's dashboard

---

### Test 3: Vendor Submits Quotation

**Login as:** Vendor (the one assigned to the PR)

**Steps:**
1. Navigate to Vendor Dashboard
2. Find `PR-TEST-001` in the list
3. Click on the PR to view details
4. Review item requirements:
   - Item Type: Building Materials
   - Description: Need 100 bags of cement
   - Quantity: 100 bags
   - Specifications: Portland cement details
5. Click "Submit Quotation"
6. In the update form (should only see quotation fields):
   - Estimated Price: `5000.00`
   - Quotation Notes: 
     ```
     Price Breakdown:
     - Cement: €45 per bag x 100 = €4,500
     - Delivery: €300
     - Handling: €200
     Total: €5,000
     
     Valid for 30 days
     Payment terms: Net 30
     ```
7. Click "Submit Quotation"

**Expected Results:**
- ✅ Quotation submitted successfully
- ✅ Only quotation fields visible in form
- ✅ Item details visible but read-only
- ✅ Cannot change status or vendor
- ✅ Quotation date and submitted_by recorded automatically

**Verify:**
- PR detail page shows "Quotation Submitted" badge
- Estimated price displays as €5,000
- Quotation notes visible in detail page
- Quotation date and vendor name shown
- Price card shows "€5,000 (Pending Approval)"

---

### Test 4: Buyer Reviews and Approves Quotation

**Login as:** Buyer

**Steps:**
1. Navigate to Buyer Dashboard
2. Find `PR-TEST-001` (should show quotation submitted)
3. Click on the PR to view details
4. Review the quotation section:
   - Estimated Price: €5,000
   - Quotation Notes: Price breakdown
5. Click "Update PR"
6. In the update form:
   - Approved Price: `5000.00` (or negotiate different amount)
   - Status: Change to `Approval`
7. Click "Approve & Update"

**Expected Results:**
- ✅ Price approved successfully
- ✅ Status changed to "Approval"
- ✅ price_approved set to True
- ✅ price_approved_by records buyer username
- ✅ price_approved_date recorded
- ✅ Final price set in total field

**Verify:**
- PR detail page shows "Price Approved!" badge
- Shows approval details (approved by, date)
- Final approved price displayed
- Price card shows "€5,000 (Final Price)"
- Status badge shows "Approval"

---

## Test 2: Dynamic Item Type Dropdown

### Test Different Categories

**Login as:** Requester

**Test Construction Category:**
1. Create new PR
2. Select Category: `Construction`
3. Verify Item Type dropdown shows:
   - Building Materials
   - Cement & Concrete
   - Steel & Metal
   - Wood & Timber
   - Electrical Materials
   - Plumbing Materials
   - Paint & Coating
   - Tiles & Flooring
   - Doors & Windows
   - Roofing Materials
   - Construction Equipment
   - Safety Equipment
   - Other Construction

**Test Information Technology Category:**
1. Change Category to: `Information Technology`
2. Verify Item Type dropdown updates to show:
   - Computer Hardware
   - Computer Software
   - Networking Equipment
   - Servers & Storage
   - Printers & Scanners
   - Mobile Devices
   - IT Services
   - Cloud Services
   - Software Licenses
   - IT Security
   - Website Development
   - Database Services
   - Other IT

**Test Office Supplies Category:**
1. Change Category to: `Office Supplies`
2. Verify Item Type dropdown updates to show:
   - Paper Products
   - Writing Instruments
   - Filing & Storage
   - Desk Accessories
   - Binding & Laminating
   - Presentation Supplies
   - Mailing Supplies
   - Cleaning Supplies
   - Breakroom Supplies
   - Office Electronics
   - Other Office Supplies

**Expected Results:**
- ✅ Dropdown updates immediately on category change
- ✅ No page reload required
- ✅ Previous selection cleared when category changes
- ✅ All item types relevant to selected category

---

## Test 3: Role-Based Permissions

### Test Requester Permissions

**Login as:** Requester

**Test Create:**
- ✅ Can create new PRs
- ✅ Cannot enter price
- ✅ Can select category and item type

**Test Edit:**
- ✅ Can edit own PRs when status is "Open"
- ❌ Cannot edit PRs when status is "Pending" or later
- ❌ Cannot assign vendors
- ❌ Cannot submit quotations

**Test Delete:**
- ✅ Can delete own PRs when status is "Open"
- ❌ Cannot delete PRs when status is "Pending" or later

---

### Test Vendor Permissions

**Login as:** Vendor

**Test View:**
- ✅ Can view PRs assigned to them
- ✅ Can see item details
- ❌ Cannot see other vendors' PRs

**Test Update:**
- ✅ Can submit quotation for assigned PRs
- ✅ Can update quotation before buyer approval
- ❌ Cannot change item details
- ❌ Cannot change status
- ❌ Cannot assign vendors

**Test Create/Delete:**
- ❌ Cannot create PRs
- ❌ Cannot delete PRs

---

### Test Buyer Permissions

**Login as:** Buyer

**Test View:**
- ✅ Can view all PRs
- ✅ Can see all quotations

**Test Update:**
- ✅ Can assign vendors
- ✅ Can approve quotations
- ✅ Can change status
- ✅ Can update payment information
- ❌ Cannot edit item details (requester only)
- ❌ Cannot submit quotations (vendor only)

**Test Create/Delete:**
- ❌ Cannot create PRs
- ❌ Cannot delete PRs

---

### Test Admin Permissions

**Login as:** Admin

**Test All Actions:**
- ✅ Can create PRs
- ✅ Can edit any PR
- ✅ Can delete any PR
- ✅ Can assign vendors
- ✅ Can approve quotations
- ✅ Can change any field
- ✅ Full access to all features

---

## Test 4: Edge Cases

### Test 1: Vendor Not Assigned
**Scenario:** Vendor tries to access PR not assigned to them

**Steps:**
1. Login as Vendor
2. Try to access PR assigned to different vendor
3. Try to update the PR

**Expected Results:**
- ❌ Cannot update PR
- ✅ Shows message "This PR is not assigned to you"

---

### Test 2: Requester Edits After Vendor Assignment
**Scenario:** Requester tries to edit PR after vendor is assigned

**Steps:**
1. Login as Requester
2. Try to edit PR with status "Pending"
3. Try to update item details

**Expected Results:**
- ✅ Can view PR details
- ❌ Cannot edit PR
- ✅ Shows message "This PR is being processed and cannot be edited"

---

### Test 3: Category Change Preserves Item Type
**Scenario:** Edit existing PR and change category

**Steps:**
1. Create PR with Category: Construction, Item Type: Building Materials
2. Save PR
3. Edit PR and change Category to IT
4. Check Item Type dropdown

**Expected Results:**
- ✅ Item Type dropdown updates to IT options
- ✅ Previous selection cleared
- ✅ Can select new item type from IT category

---

### Test 4: Multiple Quotation Updates
**Scenario:** Vendor updates quotation multiple times

**Steps:**
1. Vendor submits initial quotation: €5,000
2. Vendor updates quotation: €4,800
3. Vendor updates again: €4,500

**Expected Results:**
- ✅ Each update overwrites previous quotation
- ✅ Quotation date updates to latest submission
- ✅ Only latest quotation visible
- ✅ Buyer sees most recent quotation

---

## Test 5: UI/UX Testing

### Test Form Styling
- ✅ Form fields have rounded corners
- ✅ Focus state shows blue border
- ✅ Labels are bold and clear
- ✅ Help text is visible and helpful
- ✅ Buttons have hover effects
- ✅ Character counter for textareas

### Test Responsive Design
- ✅ Forms work on mobile devices
- ✅ Buttons stack vertically on small screens
- ✅ Cards adjust to screen size
- ✅ Text remains readable

### Test Animations
- ✅ Page slides up on load
- ✅ Buttons have hover animations
- ✅ Form fields animate on focus
- ✅ Smooth transitions

---

## Common Issues and Solutions

### Issue: Item Type dropdown not updating
**Check:**
- Browser console for JavaScript errors
- jQuery is loaded
- AJAX URL is correct: `/api/get-item-types/`
- Category field has correct ID: `id_category`

**Solution:**
- Clear browser cache
- Check network tab for AJAX request
- Verify URL pattern in urls.py

---

### Issue: Vendor cannot see assigned PRs
**Check:**
- Vendor profile exists and is linked to user
- Vendor is approved (is_approved=True)
- Vendor status is "Active"
- PR has vendor assigned

**Solution:**
- Verify vendor approval in admin panel
- Check vendor.user matches logged-in user
- Ensure PR.vendor is set correctly

---

### Issue: Quotation not saving
**Check:**
- Vendor is assigned to PR
- Form fields are not disabled
- estimated_price is a valid number
- User has vendor role

**Solution:**
- Check form validation errors
- Verify vendor permissions
- Check browser console for errors

---

## Success Criteria

The quotation workflow is working correctly when:

✅ Requesters can create PRs with item details (no price)  
✅ Item type dropdown updates based on category selection  
✅ Buyers can assign approved vendors to PRs  
✅ Vendors can submit quotations for assigned PRs  
✅ Buyers can review and approve quotations  
✅ All role-based permissions work correctly  
✅ PR detail page shows quotation information  
✅ Status flow works: Open → Pending → Approval  
✅ Audit trail records all actions (who, when)  
✅ UI is responsive and user-friendly  

---

## Next Steps After Testing

Once testing is complete:

1. ✅ Document any bugs found
2. ✅ Create test user accounts for each role
3. ✅ Train users on the workflow
4. ✅ Set up vendor approval process
5. ✅ Configure email notifications (optional)
6. ✅ Set up backup procedures
7. ✅ Monitor system performance

---

## Support

If you encounter issues during testing:

1. Check the QUOTATION_WORKFLOW_GUIDE.md for detailed workflow information
2. Review the QUICK_START.md for setup instructions
3. Check Django logs for error messages
4. Verify database migrations are applied
5. Ensure all dependencies are installed

For additional help, contact the system administrator.
