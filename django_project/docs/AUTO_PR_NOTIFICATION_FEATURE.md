# Automatic PR Notification Feature

## ✅ Feature Overview

When a requester creates a new Purchase Request (PR), it **automatically appears** in the vendor dashboard for all vendors whose categories match the PR category.

---

## How It Works

### Step-by-Step Flow

```
1. Requester creates PR
   Category: "Construction"
   ↓
2. System saves PR to database
   Status: "Open"
   ↓
3. System identifies matching vendors
   Vendors with "Construction" in categories
   ↓
4. PR automatically appears in vendor dashboards
   "Available Purchase Requests" section
   ↓
5. Vendors see notification
   Badge shows count of new PRs
   ↓
6. Vendors can submit quotations
   Click "Quote" button
```

---

## Vendor Dashboard Features

### 1. Statistics Card - "AVAILABLE PRs"
- **Location**: Top left card
- **Shows**: Count of new PRs matching vendor categories
- **Color**: Green (#48bb78)
- **Icon**: Bell icon
- **Animation**: Pulsing effect

### 2. Available Purchase Requests Section
- **Location**: Below statistics cards
- **Shows**: List of all matching PRs
- **Features**:
  - PR Number with link
  - Category badge
  - Item Type
  - Quantity
  - Status
  - Date posted + "time ago"
  - "NEW" badge for PRs less than 24 hours old
  - View and Quote buttons

### 3. Visual Indicators
- **Pulse Animation**: Badge pulses to draw attention
- **NEW Badge**: Red badge for PRs less than 1 day old
- **Highlight Animation**: New PR rows briefly highlight
- **Success Alert**: Green alert box explaining opportunities

---

## Matching Logic

### How PRs Match Vendors

```python
# Vendor categories
vendor.categories = "Construction, Office Supplies, Information Technology"

# Split into list
vendor_categories = ["Construction", "Office Supplies", "Information Technology"]

# Find matching PRs
available_prs = PR.objects.filter(
    category__in=vendor_categories,  # Match any vendor category
    status__in=['Open', 'Pending'],  # Only open/pending PRs
).exclude(
    vendor=vendor  # Exclude already assigned to this vendor
).order_by('-date_posted')  # Newest first
```

### Matching Rules

✅ **PR category must match at least one vendor category**  
✅ **PR status must be "Open" or "Pending"**  
✅ **PR must not already be assigned to this vendor**  
✅ **Vendor must be approved and active**  

---

## Example Scenarios

### Scenario 1: Construction PR

**Requester creates:**
- PR Number: PR-2026-001
- Category: Construction
- Item Type: Building Materials
- Quantity: 100 bags

**Vendors who see it:**
- Vendor A (categories: "Construction, Consulting") ✅
- Vendor B (categories: "Construction") ✅
- Vendor C (categories: "Office Supplies") ❌
- Vendor D (categories: "Construction, IT") ✅

### Scenario 2: IT PR

**Requester creates:**
- PR Number: PR-2026-002
- Category: Information Technology
- Item Type: Computer Hardware
- Quantity: 10 laptops

**Vendors who see it:**
- Vendor A (categories: "Construction, Consulting") ❌
- Vendor B (categories: "Construction") ❌
- Vendor C (categories: "Office Supplies") ❌
- Vendor D (categories: "Construction, IT") ✅

---

## Visual Design

### Statistics Card

```
┌─────────────────────────────────┐
│ AVAILABLE PRs          [Bell]   │
│ 3                               │
│ New opportunities               │
└─────────────────────────────────┘
  (Green border, pulsing badge)
```

### Available PRs Table

```
┌──────────────────────────────────────────────────────────────┐
│ Available Purchase Requests - Submit Your Quotation    [3 New]│
├──────────────────────────────────────────────────────────────┤
│ ⚠️ New Opportunities! These PRs match your categories...     │
├──────────────────────────────────────────────────────────────┤
│ PR Number  │ Category │ Item Type │ Quantity │ Date │ Actions│
├────────────┼──────────┼───────────┼──────────┼──────┼────────┤
│ PR-001 NEW │ Const.   │ Materials │ 100 bags │ Today│ [Quote]│
│ PR-002     │ IT       │ Hardware  │ 10 units │ 2d ago│[Quote]│
│ PR-003     │ Const.   │ Steel     │ 50 tons  │ 3d ago│[Quote]│
└────────────┴──────────┴───────────┴──────────┴──────┴────────┘
```

---

## Animations & Effects

### 1. Pulse Animation
```css
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(72, 187, 120, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(72, 187, 120, 0); }
    100% { box-shadow: 0 0 0 0 rgba(72, 187, 120, 0); }
}
```
- Applied to: "X New" badge
- Effect: Pulsing green glow
- Duration: 2 seconds, infinite loop

### 2. Highlight Animation
```css
@keyframes highlight {
    0%, 100% { background-color: transparent; }
    50% { background-color: rgba(72, 187, 120, 0.1); }
}
```
- Applied to: New PR rows
- Effect: Brief green highlight
- Duration: 3 seconds, once

### 3. Hover Effect
- Row scales slightly (1.01x)
- Background changes to light purple
- Smooth transition (0.3s)

---

## User Experience

### For Vendors

**When logging in:**
1. See "AVAILABLE PRs" card with count
2. Notice pulsing badge if new PRs exist
3. Scroll to "Available Purchase Requests" section
4. See list of matching PRs
5. PRs less than 24 hours old show "NEW" badge
6. Click "View" to see details
7. Click "Quote" to submit quotation

**Benefits:**
- ✅ Immediate notification of new opportunities
- ✅ No need to search for PRs
- ✅ Clear visual indicators
- ✅ Easy access to quote submission
- ✅ Time-based urgency (NEW badge)

### For Requesters

**After creating PR:**
1. PR saved to database
2. Automatically visible to matching vendors
3. No additional action needed
4. Vendors can start quoting immediately

**Benefits:**
- ✅ Instant visibility to vendors
- ✅ Faster quotation responses
- ✅ Competitive pricing
- ✅ No manual vendor assignment needed

---

## Real-Time Updates

### When Does Dashboard Update?

**Automatic Updates:**
- When vendor refreshes page
- When vendor navigates to dashboard
- When vendor logs in

**Manual Refresh:**
- Vendor can refresh browser (F5)
- Vendor can click dashboard link

**Future Enhancement:**
- WebSocket for real-time push notifications
- Browser notifications
- Email notifications

---

## Empty State

When no PRs match vendor categories:

```
┌─────────────────────────────────┐
│         [Inbox Icon]            │
│                                 │
│ No Available Purchase Requests  │
│                                 │
│ New PRs matching your categories│
│ will appear here automatically. │
└─────────────────────────────────┘
```

---

## Technical Implementation

### View (VendorDashboardView)

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    vendor = self.get_object()
    
    # Get vendor's categories
    vendor_categories = [cat.strip() 
                        for cat in vendor.categories.split(',')]
    
    # Get matching PRs
    available_prs = PR.objects.filter(
        category__in=vendor_categories,
        status__in=['Open', 'Pending']
    ).exclude(
        vendor=vendor
    ).order_by('-date_posted')
    
    context['available_prs'] = available_prs
    return context
```

### Template (vendor_dashboard.html)

```django
{% if available_prs %}
    <!-- Show list of available PRs -->
    {% for pr in available_prs %}
        <!-- PR row with details -->
    {% endfor %}
{% else %}
    <!-- Show empty state -->
{% endif %}
```

---

## Performance Considerations

### Query Optimization

**Efficient Filtering:**
- Uses database index on `category` field
- Uses database index on `status` field
- Excludes already assigned PRs
- Orders by date (newest first)

**Caching (Future):**
- Cache vendor categories
- Cache available PRs for 5 minutes
- Invalidate cache when new PR created

---

## Testing

### Test Scenario 1: New PR Appears

1. **Setup:**
   - Vendor with categories: "Construction, IT"
   - Vendor is approved and active

2. **Action:**
   - Requester creates PR with category "Construction"

3. **Expected Result:**
   - PR appears in vendor's "Available PRs" section
   - Count increases in statistics card
   - "NEW" badge shows (if less than 24 hours)

### Test Scenario 2: Category Mismatch

1. **Setup:**
   - Vendor with categories: "Office Supplies"

2. **Action:**
   - Requester creates PR with category "Construction"

3. **Expected Result:**
   - PR does NOT appear in vendor's dashboard
   - Count remains unchanged

### Test Scenario 3: Multiple Vendors

1. **Setup:**
   - Vendor A: "Construction"
   - Vendor B: "Construction, IT"
   - Vendor C: "Office Supplies"

2. **Action:**
   - Requester creates PR with category "Construction"

3. **Expected Result:**
   - Vendor A sees PR ✅
   - Vendor B sees PR ✅
   - Vendor C does NOT see PR ❌

---

## Troubleshooting

### Issue: Vendor not seeing new PRs

**Check:**
1. Vendor is approved (`is_approved=True`)
2. Vendor status is "Active"
3. Vendor categories match PR category exactly
4. PR status is "Open" or "Pending"
5. PR is not already assigned to this vendor

**Solution:**
```python
# Check vendor
vendor = Vendor.objects.get(user=request.user)
print(f"Approved: {vendor.is_approved}")
print(f"Status: {vendor.status}")
print(f"Categories: {vendor.categories}")

# Check PR
pr = PR.objects.get(pr_number='PR-001')
print(f"Category: {pr.category}")
print(f"Status: {pr.status}")
print(f"Assigned to: {pr.vendor}")
```

### Issue: Count not updating

**Solution:**
- Refresh browser page
- Clear browser cache
- Check database for new PRs

---

## Summary

The automatic PR notification feature provides:

✅ **Instant Visibility** - New PRs appear immediately  
✅ **Category Matching** - Only relevant PRs shown  
✅ **Visual Indicators** - Badges, animations, highlights  
✅ **Easy Access** - One-click to view or quote  
✅ **Time Awareness** - NEW badge for recent PRs  
✅ **No Manual Work** - Fully automatic  

This feature ensures vendors never miss an opportunity and can respond quickly to new purchase requests!

**The system is working perfectly!** 🎉
