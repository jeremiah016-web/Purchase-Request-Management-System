# Role-Based Dashboard Guide

## Overview

Each user role has a dedicated dashboard tailored to their specific workflow and responsibilities.

---

## Dashboard URLs

### Auto-Redirect (Recommended):
```
http://localhost:8000/dashboard/
```
Automatically redirects to the appropriate dashboard based on user role.

### Direct Access:
- **Requester Dashboard**: http://localhost:8000/dashboard/requester/
- **Buyer Dashboard**: http://localhost:8000/dashboard/buyer/
- **Admin Dashboard**: http://localhost:8000/dashboard/admin/

---

## 1. Requester Dashboard

**URL**: http://localhost:8000/dashboard/requester/

### Features:

#### Statistics Cards:
- **Total Requests**: All PRs created by the user
- **Open**: PRs waiting for buyer review
- **Pending**: PRs under buyer review
- **Approved**: PRs approved by buyer

#### Quick Actions:
- **Create New PR**: Submit a new purchase request
- **View All My PRs**: See complete PR history
- **My Profile**: Update account settings

#### My Purchase Requests Table:
- View all your PRs with status
- Edit PRs that are still "Open"
- View details of any PR
- See approval/rejection notes from buyers

### Workflow:
1. Login as Requester
2. Redirected to Requester Dashboard
3. Click "Create New PR" to submit request
4. Fill in PR details (status automatically set to "Open")
5. Monitor status changes in dashboard
6. View buyer notes when status changes

### Permissions:
- ✅ Create new PRs
- ✅ View own PRs
- ✅ Edit own PRs (only when status is "Open")
- ❌ Cannot approve/reject PRs
- ❌ Cannot delete PRs
- ❌ Cannot see other users' PRs

---

## 2. Buyer Dashboard

**URL**: http://localhost:8000/dashboard/buyer/

### Features:

#### Statistics Cards:
- **Open**: New requests waiting for review
- **Pending**: Requests under review
- **Approval**: Approved requests
- **On Hold**: Requests waiting for information

#### Purchase Requests Requiring Action:
- Table showing all Open and Pending PRs
- Requester information with profile picture
- Quick action buttons:
  - **Approve** (Green): Approve the request
  - **Reject** (Red): Reject the request
  - **View**: See full details

### Workflow:
1. Login as Buyer
2. Redirected to Buyer Dashboard
3. See all PRs needing attention
4. Click "Approve" or "Reject" for each PR
5. Add approval/rejection notes
6. Submit - PR status updated automatically

### Approval Process:
- Click **Approve** → Add optional notes → Status changes to "Approval"
- Click **Reject** → Add required reason → Status changes to "Closed"
- Notes are added to PR with buyer's name

### Permissions:
- ✅ View all PRs
- ✅ Approve any PR
- ✅ Reject any PR
- ✅ Update PR status
- ✅ Add notes to PRs
- ✅ Create new PRs
- ❌ Cannot delete PRs

---

## 3. Admin Dashboard

**URL**: http://localhost:8000/dashboard/admin/

### Features:

#### System Statistics:
- **Total PRs**: All purchase requests in system
- **Total Users**: All registered users
- **Open PRs**: Requests waiting for review
- **Pending**: Requests under review

#### PR Status Breakdown:
- Visual breakdown of all PR statuses
- Open, Pending, Approval, Done, On Hold, Closed counts
- Quick overview of system health

#### User Roles Distribution:
- Number of Admins, Buyers, and Requesters
- Visual progress bars showing distribution
- Percentage of each role

#### Quick Actions:
- **Buyer View**: Switch to buyer dashboard
- **Django Admin**: Access full admin panel
- **All PRs**: View all purchase requests
- **Archive**: View closed requests

#### Recent Activity:
- Latest 20 purchase requests
- Quick edit and delete actions
- Full system overview

### Workflow:
1. Login as Admin
2. Redirected to Admin Dashboard
3. Monitor system statistics
4. Access any dashboard (Buyer/Requester)
5. Manage users via Django Admin
6. Edit or delete any PR

### Permissions:
- ✅ All Buyer permissions
- ✅ All Requester permissions
- ✅ Delete any PR
- ✅ Edit all PR fields
- ✅ Access Django Admin panel
- ✅ Manage users
- ✅ Full system control

---

## Dashboard Comparison

| Feature | Requester | Buyer | Admin |
|---------|-----------|-------|-------|
| View Own PRs | ✅ | ✅ | ✅ |
| View All PRs | ❌ | ✅ | ✅ |
| Create PR | ✅ | ✅ | ✅ |
| Edit Own PR (Open) | ✅ | ✅ | ✅ |
| Edit Any PR | ❌ | ✅ | ✅ |
| Approve PR | ❌ | ✅ | ✅ |
| Reject PR | ❌ | ✅ | ✅ |
| Delete PR | ❌ | ❌ | ✅ |
| User Management | ❌ | ❌ | ✅ |
| System Statistics | ❌ | Partial | ✅ Full |

---

## Testing the Dashboards

### Step 1: Create Test Accounts

**Requester:**
```
Username: test_requester
Email: requester@test.com
Role: Requester
Password: TestPass123!
```

**Buyer:**
```
Username: test_buyer
Email: buyer@test.com
Role: Buyer
Password: TestPass123!
```

**Admin:** (already created)
```
Username: admin
Email: admin@example.com
Role: Admin
```

### Step 2: Test Requester Dashboard

1. Login as `test_requester`
2. Should redirect to: http://localhost:8000/dashboard/requester/
3. See statistics for your PRs (should be 0)
4. Click "Create New PR"
5. Submit a PR
6. Return to dashboard - see updated statistics

### Step 3: Test Buyer Dashboard

1. Logout and login as `test_buyer`
2. Should redirect to: http://localhost:8000/dashboard/buyer/
3. See the PR created by requester
4. Click "Approve" button
5. Add approval note
6. Submit - PR status changes to "Approval"

### Step 4: Test Admin Dashboard

1. Logout and login as `admin`
2. Should redirect to: http://localhost:8000/dashboard/admin/
3. See system-wide statistics
4. See all users and PRs
5. Click "Buyer View" to switch to buyer dashboard
6. Click "Django Admin" for full admin panel

---

## Navigation Tips

### After Login:
- Users are automatically redirected to their role-specific dashboard
- Dashboard URL: http://localhost:8000/dashboard/

### Switching Dashboards (Admin Only):
- Admins can access any dashboard
- Use quick action buttons on admin dashboard
- Or navigate directly to URLs

### Accessing from Anywhere:
- Add "Dashboard" link to navigation menu
- Bookmark your dashboard URL
- Use the auto-redirect URL for convenience

---

## Customization

### Adding Dashboard Links to Navigation:

Edit `prs/templates/prs/layout.html` and add:

```html
<li class="nav-item">
    <a class="nav-link" href="{% url 'dashboard' %}">
        <i class="fas fa-tachometer-alt mr-1"></i>Dashboard
    </a>
</li>
```

### Changing Default Redirect:

Edit `django_project/settings.py`:

```python
# Redirect to specific dashboard instead of auto-detect
LOGIN_REDIRECT_URL = 'requester-dashboard'  # or 'buyer-dashboard' or 'admin-dashboard'
```

---

## Dashboard Features Summary

### Requester Dashboard:
- 📊 Personal statistics
- ➕ Quick PR creation
- 📋 My PRs list
- ✏️ Edit open PRs
- 👁️ View all my PRs

### Buyer Dashboard:
- 📊 System-wide PR statistics
- ✅ Approve requests
- ❌ Reject requests
- 📋 PRs requiring action
- 🔍 View all PRs

### Admin Dashboard:
- 📊 Complete system statistics
- 👥 User role distribution
- 📈 PR status breakdown
- ⚙️ Django admin access
- 🔄 Switch between views
- 🗑️ Delete any PR

---

## Benefits

✅ **Role-Specific**: Each dashboard shows only relevant information
✅ **Efficient**: Quick access to common tasks
✅ **Clear**: Visual statistics and status indicators
✅ **Intuitive**: Easy navigation and actions
✅ **Secure**: Role-based access control
✅ **Responsive**: Works on all devices

---

## Troubleshooting

### Redirected to wrong dashboard:
- Check your profile role at http://localhost:8000/profile/
- Logout and login again
- Contact admin to update your role

### Can't access buyer/admin dashboard:
- Ensure you have the correct role
- Only Buyers can access Buyer Dashboard
- Only Admins can access Admin Dashboard

### Statistics not updating:
- Refresh the page
- Clear browser cache
- Check if PRs are actually created

### Dashboard looks broken:
- Ensure JavaScript is enabled
- Check browser console for errors
- Try a different browser

---

## Next Steps

1. **Login** and explore your dashboard
2. **Create test PRs** to see statistics update
3. **Test the workflow** between roles
4. **Customize** dashboard links in navigation
5. **Train users** on their specific dashboard

The role-based dashboards are now ready to use! 🎉
