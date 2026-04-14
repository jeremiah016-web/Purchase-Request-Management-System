from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

status_choice = (
    ('Open','Open'),
    ('Pending','Pending'),
    ('Approval','Approval'),
    ('On Hold','On Hold'),
    ('Closed','Closed')
)

category_choice = (
    ('Construction', 'Construction'),
    ('Consulting','Consulting'),
    ('Facility Management', 'Facility Management'),
    ('General Goods and Services','General Goods and Services'),
    ('Information Technology','Information Technology'),
    ('Office Supplies','Office Supplies')
)

# Item type choices for each category
ITEM_TYPE_CHOICES = {
    'Construction': (
        ('Building Materials', 'Building Materials'),
        ('Cement & Concrete', 'Cement & Concrete'),
        ('Steel & Metal', 'Steel & Metal'),
        ('Wood & Timber', 'Wood & Timber'),
        ('Electrical Materials', 'Electrical Materials'),
        ('Plumbing Materials', 'Plumbing Materials'),
        ('Paint & Coating', 'Paint & Coating'),
        ('Tiles & Flooring', 'Tiles & Flooring'),
        ('Doors & Windows', 'Doors & Windows'),
        ('Roofing Materials', 'Roofing Materials'),
        ('Construction Equipment', 'Construction Equipment'),
        ('Safety Equipment', 'Safety Equipment'),
        ('Other Construction', 'Other Construction'),
    ),
    'Consulting': (
        ('Business Consulting', 'Business Consulting'),
        ('IT Consulting', 'IT Consulting'),
        ('Financial Consulting', 'Financial Consulting'),
        ('Legal Consulting', 'Legal Consulting'),
        ('HR Consulting', 'HR Consulting'),
        ('Marketing Consulting', 'Marketing Consulting'),
        ('Management Consulting', 'Management Consulting'),
        ('Strategy Consulting', 'Strategy Consulting'),
        ('Technical Consulting', 'Technical Consulting'),
        ('Training & Development', 'Training & Development'),
        ('Other Consulting', 'Other Consulting'),
    ),
    'Facility Management': (
        ('Cleaning Services', 'Cleaning Services'),
        ('Security Services', 'Security Services'),
        ('Maintenance Services', 'Maintenance Services'),
        ('HVAC Services', 'HVAC Services'),
        ('Landscaping', 'Landscaping'),
        ('Pest Control', 'Pest Control'),
        ('Waste Management', 'Waste Management'),
        ('Catering Services', 'Catering Services'),
        ('Reception Services', 'Reception Services'),
        ('Parking Management', 'Parking Management'),
        ('Building Management', 'Building Management'),
        ('Other Facility Services', 'Other Facility Services'),
    ),
    'General Goods and Services': (
        ('Office Furniture', 'Office Furniture'),
        ('Stationery', 'Stationery'),
        ('Printing Services', 'Printing Services'),
        ('Courier Services', 'Courier Services'),
        ('Transportation', 'Transportation'),
        ('Catering', 'Catering'),
        ('Uniforms', 'Uniforms'),
        ('Promotional Items', 'Promotional Items'),
        ('Packaging Materials', 'Packaging Materials'),
        ('General Supplies', 'General Supplies'),
        ('Other Goods', 'Other Goods'),
    ),
    'Information Technology': (
        ('Computer Hardware', 'Computer Hardware'),
        ('Computer Software', 'Computer Software'),
        ('Networking Equipment', 'Networking Equipment'),
        ('Servers & Storage', 'Servers & Storage'),
        ('Printers & Scanners', 'Printers & Scanners'),
        ('Mobile Devices', 'Mobile Devices'),
        ('IT Services', 'IT Services'),
        ('Cloud Services', 'Cloud Services'),
        ('Software Licenses', 'Software Licenses'),
        ('IT Security', 'IT Security'),
        ('Website Development', 'Website Development'),
        ('Database Services', 'Database Services'),
        ('Other IT', 'Other IT'),
    ),
    'Office Supplies': (
        ('Paper Products', 'Paper Products'),
        ('Writing Instruments', 'Writing Instruments'),
        ('Filing & Storage', 'Filing & Storage'),
        ('Desk Accessories', 'Desk Accessories'),
        ('Binding & Laminating', 'Binding & Laminating'),
        ('Presentation Supplies', 'Presentation Supplies'),
        ('Mailing Supplies', 'Mailing Supplies'),
        ('Cleaning Supplies', 'Cleaning Supplies'),
        ('Breakroom Supplies', 'Breakroom Supplies'),
        ('Office Electronics', 'Office Electronics'),
        ('Other Office Supplies', 'Other Office Supplies'),
    ),
}

payment_status_choice = (
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
    ('Partially Paid', 'Partially Paid'),
    ('Cancelled', 'Cancelled')
)

delivery_status_choice = (
    ('Not Shipped', 'Not Shipped'),
    ('In Transit', 'In Transit'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)

vendor_status_choice = (
    ('Pending', 'Pending Approval'),
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
    ('Blacklisted', 'Blacklisted')
)


class Vendor(models.Model):
    """Vendor/Supplier information"""
    # User account link
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='vendor_profile')
    
    name = models.CharField(max_length=200, unique=True)
    contact_person = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    # Business details
    tax_id = models.CharField(max_length=100, blank=True, help_text="Tax ID or Business Registration Number")
    bank_account = models.CharField(max_length=100, blank=True)
    account_holder = models.CharField(max_length=200, blank=True, help_text="Bank account holder name")
    ifsc_code = models.CharField(max_length=20, blank=True, help_text="IFSC code for bank transfer")
    upi_id = models.CharField(max_length=100, blank=True, help_text="UPI ID for payments (e.g. vendor@upi)")
    payment_terms = models.CharField(max_length=100, blank=True, help_text="e.g., Net 30, Net 60")
    
    # Categories they serve - now using MultipleChoiceField approach
    categories = models.CharField(
        max_length=500, 
        blank=True, 
        help_text="Select categories you serve (comma-separated)"
    )
    
    # Status and ratings
    status = models.CharField(max_length=50, choices=vendor_status_choice, default='Pending')
    rating = models.FloatField(default=0.0, help_text="Average rating out of 5")
    
    # Approval tracking
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendors_approved')
    approved_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    date_added = models.DateTimeField(default=timezone.now)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='vendors_added')
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('vendor-detail', kwargs={'pk': self.pk})
    
    def total_orders(self):
        return self.pr_set.count()
    
    def total_value(self):
        return sum(pr.total for pr in self.pr_set.all())
    
    def get_categories_list(self):
        """Return categories as a list"""
        if self.categories:
            return [cat.strip() for cat in self.categories.split(',')]
        return []
    
    def set_categories_list(self, categories_list):
        """Set categories from a list"""
        self.categories = ', '.join(categories_list)


class VendorContact(models.Model):
    """Track communications with vendors"""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='contacts')
    pr = models.ForeignKey('PR', on_delete=models.CASCADE, null=True, blank=True, related_name='vendor_contacts')
    
    contact_type = models.CharField(max_length=50, choices=(
        ('Email', 'Email'),
        ('Phone', 'Phone'),
        ('Meeting', 'Meeting'),
        ('Other', 'Other')
    ))
    
    subject = models.CharField(max_length=200)
    message = models.TextField()
    response = models.TextField(blank=True)
    
    contacted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contact_date = models.DateTimeField(default=timezone.now)
    follow_up_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-contact_date']
    
    def __str__(self):
        return f"{self.vendor.name} - {self.subject}"


class VendorQuotation(models.Model):
    """Track multiple vendor quotations for each PR"""
    pr = models.ForeignKey('PR', on_delete=models.CASCADE, related_name='quotations')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='quotations')
    
    estimated_price = models.FloatField(help_text="Vendor's quoted price")
    quotation_notes = models.TextField(blank=True, help_text="Price breakdown and details")
    quotation_date = models.DateTimeField(default=timezone.now)
    
    is_selected = models.BooleanField(default=False, help_text="Selected by buyer")
    selected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='quotations_selected')
    selected_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['estimated_price']  # Show cheapest first
        unique_together = ['pr', 'vendor']  # One quotation per vendor per PR
    
    def __str__(self):
        return f"{self.vendor.name} - {self.pr.pr_number} - €{self.estimated_price}"


class Payment(models.Model):
    """Track payments for purchase requests"""
    pr = models.ForeignKey('PR', on_delete=models.CASCADE, related_name='payments')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50, choices=(
        ('Bank Transfer', 'Bank Transfer'),
        ('Check', 'Check'),
        ('Credit Card', 'Credit Card'),
        ('Cash', 'Cash'),
        ('Other', 'Other')
    ))
    
    payment_date = models.DateField()
    reference_number = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=50, choices=payment_status_choice, default='Pending')
    
    notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment for {self.pr.pr_number} - €{self.amount}"


class Delivery(models.Model):
    """Track item delivery and shipment"""
    pr = models.ForeignKey('PR', on_delete=models.CASCADE, related_name='deliveries')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    
    tracking_number = models.CharField(max_length=100, blank=True)
    carrier = models.CharField(max_length=100, blank=True, help_text="Shipping carrier name")
    
    status = models.CharField(max_length=50, choices=delivery_status_choice, default='Not Shipped')
    
    shipped_date = models.DateField(null=True, blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    
    delivery_address = models.TextField(blank=True)
    recipient_name = models.CharField(max_length=200, blank=True)
    recipient_contact = models.CharField(max_length=100, blank=True)
    
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Deliveries'
    
    def __str__(self):
        return f"Delivery for {self.pr.pr_number} - {self.status}"
    
    def is_delayed(self):
        if self.expected_delivery_date and not self.actual_delivery_date:
            return timezone.now().date() > self.expected_delivery_date
        return False

class PR(models.Model):
    pr_number = models.CharField(max_length=100, unique=True)
    
    # Item Details (filled by requester)
    item_type = models.CharField(max_length=200, blank=True, help_text="Type of item/service needed")
    items_description = models.TextField(blank=True, help_text="Detailed description of items needed")
    quantity = models.CharField(max_length=100, blank=True, help_text="Quantity needed (e.g., 10 units, 5 boxes)")
    specifications = models.TextField(blank=True, help_text="Technical specifications or requirements")
    
    # Price/Quotation (filled by vendor)
    estimated_price = models.FloatField(null=True, blank=True, help_text="Vendor's estimated price")
    quotation_notes = models.TextField(blank=True, help_text="Vendor's quotation notes and breakdown")
    quotation_date = models.DateTimeField(null=True, blank=True)
    quotation_submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='quotations_submitted')
    
    # Final approved price
    total = models.FloatField(max_length=100, default=0.00, help_text="Final approved price")
    price_approved = models.BooleanField(default=False)
    price_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prices_approved')
    price_approved_date = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=100, choices=status_choice, default='Open')
    category = models.CharField(max_length=100, choices=category_choice, default='Choose Category')
    description = models.TextField(blank=True, default='', help_text="Additional notes and comments")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # one user can have many prs
    
    # Vendor relationship
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='pr_set')
    
    # Legacy vendor fields (kept for backward compatibility)
    vendor_name = models.CharField(max_length=200, blank=True, default='')
    vendor_contact = models.CharField(max_length=100, blank=True, default='')
    
    # Payment fields
    payment_status = models.CharField(max_length=50, choices=payment_status_choice, default='Pending')
    payment_date = models.DateField(null=True, blank=True)
    payment_notes = models.TextField(blank=True, default='')
    
    # Delivery status
    delivery_status = models.CharField(max_length=50, choices=delivery_status_choice, default='Not Shipped')

    # Requester payment & delivery address (filled when requester approves quotation)
    delivery_address = models.TextField(blank=True, default='', help_text="Delivery address provided by requester")
    requester_approved_quotation = models.BooleanField(default=False, help_text="Requester approved the quotation and paid")
    payment_transaction_id = models.CharField(max_length=200, blank=True, default='', help_text="Online payment transaction ID")
    payment_method_used = models.CharField(max_length=100, blank=True, default='', help_text="Payment method used by requester")

    def __str__(self):
        return self.pr_number

    def get_absolute_url(self):
        return reverse('pr-detail', kwargs={'pk': self.pk})
    
    def total_paid(self):
        """Calculate total amount paid"""
        return sum(payment.amount for payment in self.payments.filter(status='Paid'))
    
    def remaining_balance(self):
        """Calculate remaining balance"""
        return self.total - self.total_paid()
    
    def has_quotation(self):
        """Check if vendor has submitted quotation"""
        return self.estimated_price is not None and self.estimated_price > 0
