from django.contrib import admin
from .models import PR, Vendor, VendorContact, Payment, Delivery, VendorQuotation

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'status', 'rating', 'date_added']
    list_filter = ['status', 'date_added']
    search_fields = ['name', 'contact_person', 'email', 'phone']
    ordering = ['name']

@admin.register(VendorContact)
class VendorContactAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'subject', 'contact_type', 'contacted_by', 'contact_date']
    list_filter = ['contact_type', 'contact_date']
    search_fields = ['vendor__name', 'subject', 'message']
    ordering = ['-contact_date']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pr', 'vendor', 'amount', 'payment_method', 'payment_date', 'status', 'processed_by']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['pr__pr_number', 'vendor__name', 'reference_number']
    ordering = ['-payment_date']

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['pr', 'vendor', 'tracking_number', 'status', 'shipped_date', 'expected_delivery_date', 'actual_delivery_date']
    list_filter = ['status', 'shipped_date', 'expected_delivery_date']
    search_fields = ['pr__pr_number', 'tracking_number', 'carrier']
    ordering = ['-created_at']

@admin.register(VendorQuotation)
class VendorQuotationAdmin(admin.ModelAdmin):
    list_display = ['pr', 'vendor', 'estimated_price', 'quotation_date', 'is_selected', 'selected_by', 'selected_date']
    list_filter = ['is_selected', 'quotation_date', 'selected_date']
    search_fields = ['pr__pr_number', 'vendor__name', 'quotation_notes']
    ordering = ['-quotation_date']
    readonly_fields = ['quotation_date', 'selected_date']

admin.site.register(PR)
