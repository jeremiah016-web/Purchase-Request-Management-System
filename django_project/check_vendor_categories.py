#!/usr/bin/env python
"""Check and update vendor categories to match PR categories"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from prs.models import Vendor

# Valid PR categories
VALID_CATEGORIES = [
    'Construction',
    'Consulting',
    'Facility Management',
    'General Goods and Services',
    'Information Technology',
    'Office Supplies'
]

print(f"\n{'='*60}")
print(f"VENDOR CATEGORY CHECK")
print(f"{'='*60}\n")

print("Valid PR Categories:")
for cat in VALID_CATEGORIES:
    print(f"  - {cat}")
print()

vendors = Vendor.objects.all()
print(f"Found {vendors.count()} vendor(s):\n")

for vendor in vendors:
    print(f"📋 Vendor: {vendor.name}")
    print(f"   Current Categories: {vendor.categories}")
    print(f"   Status: {vendor.status}")
    print(f"   Approved: {vendor.is_approved}")
    
    # Parse current categories
    current_cats = [cat.strip() for cat in vendor.categories.split(',')] if vendor.categories else []
    
    # Check if any category doesn't match valid categories
    invalid_cats = [cat for cat in current_cats if cat not in VALID_CATEGORIES]
    
    if invalid_cats:
        print(f"   ⚠️  Invalid categories found: {', '.join(invalid_cats)}")
        print(f"   💡 Suggestion: Update to use valid categories from the list above")
    else:
        print(f"   ✅ All categories are valid!")
    
    print()

print(f"{'='*60}\n")
