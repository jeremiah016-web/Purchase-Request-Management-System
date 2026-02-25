#!/usr/bin/env python
"""Update vendor categories to match system categories"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from prs.models import Vendor

print(f"\n{'='*60}")
print(f"UPDATE VENDOR CATEGORIES")
print(f"{'='*60}\n")

vendor = Vendor.objects.get(name='BIRLA')

print(f"📋 Vendor: {vendor.name}")
print(f"   Old Categories: {vendor.categories}")

# Update to valid categories
# Electronics → Information Technology
# Office Supplies → Office Supplies (already valid)
# Furniture → General Goods and Services
new_categories = "Information Technology, Office Supplies, General Goods and Services"

vendor.categories = new_categories
vendor.save()

print(f"   ✅ New Categories: {vendor.categories}")
print(f"\n{'='*60}")
print(f"✅ Vendor categories updated successfully!")
print(f"{'='*60}\n")

print("Now the vendor will see PRs in these categories:")
for cat in new_categories.split(','):
    print(f"  - {cat.strip()}")
print()
