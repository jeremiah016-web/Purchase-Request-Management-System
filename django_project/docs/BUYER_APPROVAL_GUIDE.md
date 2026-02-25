# Buyer Approval System Guide

## Overview

The system now has a streamlined approval workflow where Buyers can quickly **Approve** or **Reject** purchase requests with a single click.

---

## How It Works

### For Requesters:
1. Create a purchase request (automatically set to "Open" status)
2. Wait for Buyer to review
3. Receive notification when approved or rejected

### For Buyers:
1. Login and go to **Buyer Dashboard**: http://localhost:8000/buyer/dashboard/
2. See all pending purchase requests
3. Click **"Approve"** or **"Reject"** button for each PR
4. Add optional notes (required for rejection)
5. Submit - PR status is automatically updated

### For Admins:
- All Buyer permissions
- Can manually change any status
- Can delete or modify any PR
- Full system control

---

## Buyer Dashboard Features

### Statistics Cards:
- **Open**: New requests waiting for review
- **Pending**: Requests under review
- **Approval**: Approved requests
- **On Hold**: Requests waiting for information

### Action Buttons:
- **Approve** (Green): Approve the purchase request
- **Reject** (Red): Reject the purchase request
- **View**: See full PR details

---

## Approval Process

### When Buyer Clicks "Approve":

1. Redirected to approval page showing PR details
2. Can add optional approval notes
3. Click "Approve Request" button
4. PR status changes to **"Approval"**
5. Approval note is added to PR description with buyer's name
6. Requester can see the approval

**Example approval note added:**
```
[APPROVED by sarah_buyer]: Budget approved. Proceed with purchase from Vendor X.
```

---

## Rejection Process

### When Buyer Clicks "Reject":

1. Redirected to rejection page showing PR details
2. **Must** provide a rejection reason (required field)
3. Click "Reject Request" button
4. PR status changes to **"Closed"**
5. Rejection reason is added to PR description with buyer's name
6. Requester can see why it was rejected

**Example rejection note added:**
```
[REJECTED by sarah_buyer]: Budget not available for this quarter. Please resubmit in Q2.
```

---

## Status Flow

```
Requester Creates PR
        ↓
    [Open Status]
        ↓
Buyer Reviews in Dashboard
        ↓
    ┌───────┴───────┐
    ↓               ↓
[Approve]      [Reject]
    ↓               ↓
[Approval]      [Closed]
    ↓
Buyer Processes Purchase
    ↓
[Done Status]
```

---

## URLs

### Buyer Dashboard:
```
http://localhost:8000/buyer/dashboard/
```

### Approve PR:
```
http://localhost:8000/pr/[id]/approve/
```

### Reject PR:
```
http://localhost:8000/pr/[id]/reject/
```

### Manual Update (for complex cases):
```
http://localhost:8000/pr/[id]/update/
```

---

## Testing the Approval System

### Step 1: Create Test Accounts

**Requester:**
- Go to http://localhost:8000/register/
- Username: test_requester
- Email: requester@test.com
- Role: Requester
- Password: TestPass123!

**Buyer:**
- Go to http://localhost:8000/register/
- Username: test_buyer
- Email: buyer@test.com
- Role: Buyer
- Password: TestPass123!

### Step 2: Create a Purchase Request

1. Login as `test_requester`
2. Go to http://localhost:8000/pr/new/
3. Fill in:
   - PR Number: PR-2024-001
   - Category: Office Supplies
   - Description: Need 10 boxes of printer paper
4. Submit (status automatically set to "Open")

### Step 3: Approve as Buyer

1. Logout and login as `test_buyer`
2. Go to http://localhost:8000/buyer/dashboard/
3. See the PR in the list
4. Click **"Approve"** button
5. Add note: "Approved. Budget available."
6. Click "Approve Request"
7. PR status changes to "Approval"

### Step 4: View as Requester

1. Logout and login as `test_requester`
2. Go to http://localhost:8000/
3. See your PR with "Approval" status
4. Click to view details
5. See the approval note from the buyer

---

## Advanced Features

### Manual Status Updates

Buyers can still use the manual update page for complex scenarios:
- Setting status to "Pending" (under review)
- Setting status to "On Hold" (need more info)
- Setting status to "Done" (purchase completed)
- Adding detailed notes

Access via: http://localhost:8000/pr/[id]/update/

### Admin Override

Admins can:
- Change any status manually
- Delete rejected PRs
- Reopen closed PRs
- Edit all fields including total amount

---

## Permissions Summary

| Action | Requester | Buyer | Admin |
|--------|-----------|-------|-------|
| Create PR | ✅ (Open status) | ✅ (Any status) | ✅ (Any status) |
| View PRs | ✅ All | ✅ All | ✅ All |
| Edit Own PR (Open) | ✅ | ✅ | ✅ |
| Edit Own PR (Processing) | ❌ View only | ✅ | ✅ |
| Approve PR | ❌ | ✅ | ✅ |
| Reject PR | ❌ | ✅ | ✅ |
| Delete PR | ❌ | ❌ | ✅ |
| Access Buyer Dashboard | ❌ | ✅ | ✅ |

---

## Benefits of This System

✅ **Quick Actions**: One-click approve/reject
✅ **Clear Audit Trail**: All actions logged with buyer name
✅ **Transparent**: Requesters see approval/rejection reasons
✅ **Flexible**: Can still use manual update for complex cases
✅ **Role-Based**: Proper separation of duties
✅ **User-Friendly**: Simple, intuitive interface

---

## Troubleshooting

### "Permission Denied" when trying to approve:
- Ensure you're logged in as Buyer or Admin
- Check your profile role at http://localhost:8000/profile/

### Can't see Buyer Dashboard:
- Only Buyers and Admins can access
- URL: http://localhost:8000/buyer/dashboard/
- Check your role in profile

### Approval note not showing:
- Notes are appended to the PR description
- View the full PR details to see all notes
- Format: `[APPROVED by username]: note`

### Want to undo approval:
- Admins can manually change status back
- Or use the manual update page to change status

---

## Next Steps

1. **Test the system** with the test accounts above
2. **Create real user accounts** for your team
3. **Train buyers** on using the dashboard
4. **Train requesters** on creating PRs
5. **Monitor the workflow** and adjust as needed

---

## Support

For issues or questions:
- Check `WORKFLOW_GUIDE.md` for detailed workflow
- Check `README_ROLE_BASED_AUTH.md` for authentication details
- Review `QUICK_START.md` for setup instructions

The approval system is now ready to use! 🎉
