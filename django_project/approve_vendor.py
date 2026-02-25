#!/usr/bin/env python
"""Quick script to approve pending vendors"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from prs.models import Vendor
from django.contrib.auth.models import User
from django.utils import timezone

# Get all pending vendors
pending_vendors = Vendor.objects.filter(is_approved=False)

print(f"\n{'='*60}")
print(f"VENDOR APPROVAL SCRIPT")
print(f"{'='*60}\n")

if not pending_vendors.exists():
    print("✅ No pending vendors found. All vendors are already approved!")
else:
    print(f"Found {pending_vendors.count()} pending vendor(s):\n")
    
    # Get an admin user to approve
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        admin = User.objects.filter(is_staff=True).first()
    
    for vendor in pending_vendors:
        print(f"📋 Vendor: {vendor.name}")
        print(f"   Email: {vendor.email}")
        print(f"   Categories: {vendor.categories}")
        print(f"   Current Status: {vendor.status}")
        
        # Approve the vendor
        vendor.is_approved = True
        vendor.status = 'Active'
        vendor.approved_by = admin
        vendor.approved_date = timezone.now()
        vendor.save()
        
        print(f"   ✅ APPROVED!")
        print(f"   New Status: {vendor.status}")
        print(f"   Approved by: {vendor.approved_by.username if vendor.approved_by else 'System'}")
        print(f"   Approved on: {vendor.approved_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

print(f"{'='*60}")
print(f"✅ All vendors approved successfully!")
print(f"{'='*60}\n")
