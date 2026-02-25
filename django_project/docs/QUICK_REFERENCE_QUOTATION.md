# Quick Reference: Quotation Workflow

## 🎯 Quick Overview

**Requester** → Creates PR with item details (no price)  
**Buyer** → Assigns vendor to PR  
**Vendor** → Submits price quotation  
**Buyer** → Approves final price  

---

## 👤 For Requesters

### Creating a PR
1. Click "Create New PR"
2. Fill in:
   - PR Number
   - **Category** (select first)
   - **Item Type** (auto-populates based on category)
   - Items Description
   - Quantity
   - Specifications (optional)
3. Click "Create Purchase Request"

**Note:** Don't enter price - vendors will quote!

### Editing a PR
- Can edit only when status is "Open"
- Cannot edit after vendor is assigned
- Contact buyer if changes needed

---

## 🏪 For Vendors

### Submitting a Quotation
1. Go to Vendor Dashboard
2. Find your assigned PR
3. Click "Submit Quotation"
4. Enter:
   - **Estimated Price** (required)
   - **Quotation Notes** (price breakdown)
5. Click "Submit Quotation"

### Quotation Notes Should Include:
- Itemized price breakdown
- Unit prices
- Delivery costs
- Payment terms
- Validity period

**Example:**
```
Price Breakdown:
- Item: €45 per unit x 100 = €4,500
- Delivery: €300
- Handling: €200
Total: €5,000

Valid for 30 days
Payment terms: Net 30
```

---

## 💼 For Buyers

### Assigning a Vendor
1. Go to Buyer Dashboard
2. Find the PR
3. Click "Update PR"
4. Select vendor from dropdown
5. Change status to "Pending"
6. Click "Approve & Update"

### Approving a Quotation
1. Review vendor's quotation
2. Click "Update PR"
3. Enter final price in "Approved Price"
4. Change status to "Approval"
5. Click "Approve & Update"

---

## 📊 Status Meanings

| Status | Meaning |
|--------|---------|
| **Open** | PR created, awaiting buyer action |
| **Pending** | Vendor assigned, awaiting quotation |
| **Approval** | Quotation approved, ready to proceed |
| **On Hold** | Temporarily paused |
| **Closed** | Completed or cancelled |

---

## 🏷️ Item Type Categories

### Construction
Building Materials, Cement & Concrete, Steel & Metal, Wood & Timber, Electrical Materials, Plumbing Materials, Paint & Coating, Tiles & Flooring, Doors & Windows, Roofing Materials, Construction Equipment, Safety Equipment, Other

### Consulting
Business Consulting, IT Consulting, Financial Consulting, Legal Consulting, HR Consulting, Marketing Consulting, Management Consulting, Strategy Consulting, Technical Consulting, Training & Development, Other

### Facility Management
Cleaning Services, Security Services, Maintenance Services, HVAC Services, Landscaping, Pest Control, Waste Management, Catering Services, Reception Services, Parking Management, Building Management, Other

### General Goods and Services
Office Furniture, Stationery, Printing Services, Courier Services, Transportation, Catering, Uniforms, Promotional Items, Packaging Materials, General Supplies, Other

### Information Technology
Computer Hardware, Software, Networking Equipment, Servers & Storage, Printers & Scanners, Mobile Devices, IT Services, Cloud Services, Software Licenses, IT Security, Website Development, Database Services, Other

### Office Supplies
Paper Products, Writing Instruments, Filing & Storage, Desk Accessories, Binding & Laminating, Presentation Supplies, Mailing Supplies, Cleaning Supplies, Breakroom Supplies, Office Electronics, Other

---

## ❓ Common Questions

**Q: Why can't I enter a price as a requester?**  
A: Vendors provide price quotations based on your requirements. This ensures accurate pricing.

**Q: Can I change the item type after selecting a category?**  
A: Yes! The item type dropdown updates automatically when you change the category.

**Q: What if I need to edit my PR after it's assigned to a vendor?**  
A: Contact your buyer. Only buyers can make changes after vendor assignment.

**Q: How do I know if my quotation was approved?**  
A: Check the PR detail page. It will show "Price Approved!" with approval details.

**Q: Can I submit multiple quotations?**  
A: Yes, you can update your quotation before the buyer approves it.

**Q: What happens after the price is approved?**  
A: The PR moves to payment and delivery processing.

---

## 🚨 Troubleshooting

### Item Type dropdown is empty
→ Select a category first

### Cannot submit quotation
→ Check if you're assigned to the PR  
→ Verify your vendor account is approved

### Cannot edit PR
→ Check PR status (must be "Open" for requesters)  
→ Verify you have the correct role

### Vendor not in dropdown
→ Vendor must be approved by admin  
→ Vendor status must be "Active"

---

## 📞 Need Help?

- **Workflow Details:** See QUOTATION_WORKFLOW_GUIDE.md
- **Testing Guide:** See TESTING_QUOTATION_WORKFLOW.md
- **System Setup:** See QUICK_START.md
- **Vendor Info:** See VENDOR_ASSIGNMENT_GUIDE.md

---

## ✅ Quick Checklist

### Before Creating a PR (Requester)
- [ ] Know what you need
- [ ] Have quantity information
- [ ] Have specifications ready
- [ ] Know the category

### Before Submitting Quotation (Vendor)
- [ ] Reviewed all item details
- [ ] Calculated accurate price
- [ ] Prepared price breakdown
- [ ] Included all costs (delivery, etc.)
- [ ] Specified payment terms

### Before Approving Quotation (Buyer)
- [ ] Reviewed vendor quotation
- [ ] Verified price breakdown
- [ ] Checked vendor rating
- [ ] Confirmed budget availability
- [ ] Ready to proceed with purchase

---

## 🎓 Best Practices

### Requesters
✅ Be specific in descriptions  
✅ Include all specifications  
✅ Provide accurate quantities  
✅ Add relevant notes  

### Vendors
✅ Respond promptly  
✅ Provide detailed breakdowns  
✅ Be transparent about costs  
✅ Specify validity period  

### Buyers
✅ Assign appropriate vendors  
✅ Review quotations thoroughly  
✅ Communicate with vendors  
✅ Update status promptly  

---

**Last Updated:** February 2026  
**Version:** 1.0
