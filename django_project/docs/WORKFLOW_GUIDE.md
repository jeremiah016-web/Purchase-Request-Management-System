# Purchase Request Workflow Guide

## Role-Based Workflow

### 1. Requester Role
**Purpose**: Create and submit purchase requests

**Permissions**:
- ✅ Create new purchase requests (automatically set to "Open" status)
- ✅ View all purchase requests
- ✅ Edit their own PRs (only when status is "Open")
- ✅ Update description and category of their own PRs
- ❌ Cannot change PR status
- ❌ Cannot delete PRs
- ❌ Cannot edit PRs once they're being processed (status changed from "Open")

**Workflow**:
1. Login as Requester
2. Click "New PR" to create a purchase request
3. Fill in:
   - PR Number (unique identifier)
   - Category (type of purchase)
   - Description (details of what's needed)
4. Submit - PR is automatically set to "Open" status
5. Wait for Buyer to process the request
6. Can view status updates but cannot modify once Buyer starts processing

---

### 2. Buyer Role
**Purpose**: Review, approve, and process purchase requests

**Permissions**:
- ✅ View all purchase requests
- ✅ Access Buyer Dashboard (shows PRs needing attention)
- ✅ Update any PR status (Open → Pending → Approval → Done/On Hold)
- ✅ Add notes to PR descriptions
- ✅ Create new PRs with any status
- ❌ Cannot delete PRs (only Admin can)

**Workflow**:
1. Login as Buyer
2. Go to Buyer Dashboard: http://localhost:8000/buyer/dashboard/
3. See all "Open" and "Pending" PRs that need action
4. Click "Process" on a PR to review it
5. Update the status:
   - **Pending**: Under review
   - **Approval**: Approved and ready to purchase
   - **On Hold**: Waiting for more information
   - **Done**: Purchase completed
   - **Closed**: Request closed/cancelled
6. Add notes in the description field if needed
7. Save changes

**Buyer Dashboard Features**:
- Statistics showing count of PRs by status
- List of all PRs requiring action (Open/Pending)
- Quick access to process each PR
- View requester information

---

### 3. Admin Role
**Purpose**: Full system management and oversight

**Permissions**:
- ✅ All Buyer permissions
- ✅ All Requester permissions
- ✅ Delete any PR
- ✅ Edit any PR field including total amount
- ✅ Manage users
- ✅ Access Django admin panel
- ✅ Override any restrictions

**Workflow**:
1. Login as Admin
2. Full access to all features
3. Can manage users via Django admin: http://localhost:8000/admin/
4. Can delete problematic or duplicate PRs
5. Can edit all fields including financial data
6. Oversee entire purchase request process

---

## Purchase Request Statuses

| Status | Description | Who Can Set | Next Steps |
|--------|-------------|-------------|------------|
| **Open** | New request submitted | Requester (auto) | Buyer reviews |
| **Pending** | Under review by buyer | Buyer/Admin | Buyer approves or requests info |
| **Approval** | Approved for purchase | Buyer/Admin | Buyer makes purchase |
| **On Hold** | Waiting for information | Buyer/Admin | Requester provides info |
| **Done** | Purchase completed | Buyer/Admin | Can be archived |
| **Closed** | Request cancelled/closed | Buyer/Admin | Archived |

---

## Complete Workflow Example

### Scenario: Office Supplies Purchase

1. **Requester Creates PR**:
   - Username: john_requester
   - Creates PR #2024-001
   - Category: Office Supplies
   - Description: "Need 10 boxes of printer paper and 5 toner cartridges"
   - Status: Automatically set to "Open"

2. **Buyer Reviews PR**:
   - Username: sarah_buyer
   - Sees PR #2024-001 in Buyer Dashboard
   - Clicks "Process"
   - Changes status to "Pending"
   - Adds note: "Checking inventory and pricing"

3. **Buyer Approves PR**:
   - Updates status to "Approval"
   - Adds note: "Approved. Total cost: $250. Ordering from Supplier X"

4. **Buyer Completes Purchase**:
   - Makes the purchase
   - Updates status to "Done"
   - Adds note: "Order placed. Delivery expected in 3 days"

5. **Admin Archives** (Optional):
   - Can change status to "Closed" to archive
   - Or delete if needed

---

## Access URLs

### For All Users:
- Home (All PRs): http://localhost:8000/
- My PRs: http://localhost:8000/user/[username]
- Create PR: http://localhost:8000/pr/new/
- View PR: http://localhost:8000/pr/[id]/
- Update PR: http://localhost:8000/pr/[id]/update/

### For Buyers & Admins:
- Buyer Dashboard: http://localhost:8000/buyer/dashboard/
- Buyer List: http://localhost:8000/buyers/

### For Admins Only:
- Django Admin: http://localhost:8000/admin/
- Delete PR: http://localhost:8000/post/[id]/delete/

---

## Field Permissions by Role

### Create PR Form:

| Field | Requester | Buyer | Admin |
|-------|-----------|-------|-------|
| PR Number | ✅ | ✅ | ✅ |
| Status | ❌ (auto "Open") | ✅ | ✅ |
| Category | ✅ | ✅ | ✅ |
| Description | ✅ | ✅ | ✅ |
| Total | ❌ | ❌ | ✅ |

### Update PR Form:

| Field | Requester (Own PR, Open) | Requester (Own PR, Processing) | Buyer | Admin |
|-------|--------------------------|-------------------------------|-------|-------|
| Status | ❌ | ❌ | ✅ | ✅ |
| Category | ✅ | ❌ | ❌ | ✅ |
| Description | ✅ | View Only | ✅ | ✅ |
| Total | ❌ | ❌ | ❌ | ✅ |

---

## Tips for Each Role

### For Requesters:
- Be specific in your descriptions
- Include quantity, specifications, and urgency
- Check your PR status regularly
- If status is "On Hold", check for buyer notes and provide requested information

### For Buyers:
- Check the Buyer Dashboard daily
- Update status promptly to keep requesters informed
- Add notes when changing status to explain decisions
- Use "On Hold" when you need more information from requester

### For Admins:
- Monitor overall system usage
- Delete duplicate or test PRs
- Manage user roles via Django admin
- Assist buyers with complex requests

---

## Testing the Workflow

### Create Test Users:

1. **Requester Account**:
   ```
   Username: test_requester
   Email: requester@test.com
   Role: Requester
   ```

2. **Buyer Account**:
   ```
   Username: test_buyer
   Email: buyer@test.com
   Role: Buyer
   ```

3. **Admin Account** (already created):
   ```
   Username: admin
   Email: admin@example.com
   Role: Admin
   ```

### Test Scenario:

1. Login as `test_requester`
2. Create a new PR
3. Logout and login as `test_buyer`
4. Go to Buyer Dashboard
5. Process the PR (change status)
6. Logout and login as `test_requester`
7. View the updated PR (should see status change but cannot edit)
8. Login as `admin`
9. Edit or delete the PR

---

## Troubleshooting

### "Permission Denied" Error:
- Check your user role in profile
- Ensure you're logged in
- Verify you have permission for that action

### Cannot Edit PR:
- Requesters can only edit "Open" PRs
- Once Buyer changes status, requester can only view
- Buyers and Admins can always edit

### Buyer Dashboard Not Showing:
- Ensure you're logged in as Buyer or Admin
- Check URL: http://localhost:8000/buyer/dashboard/
- Verify your profile role is set correctly

---

## Summary

✅ **Requester**: Creates requests → Waits for processing
✅ **Buyer**: Reviews requests → Updates status → Processes purchases
✅ **Admin**: Manages everything → Full control

This workflow ensures proper separation of duties and clear accountability in the purchase request process.
