from django.urls import path
from . import views
from .views import (SearchView, CategoryListView, BuyerListView, BuyerDashboardView, 
                    RequesterDashboardView, AdminDashboardView,
                    PRListView, ArchivePRListView, PRDetailView, PRCreateView, 
                    UserPRListView, PRUpdateView, PRDeleteView, PRApproveView, PRRejectView,
                    dashboard_redirect,
                    # Vendor views
                    VendorListView, VendorDetailView, VendorCreateView, VendorUpdateView, VendorDeleteView,
                    VendorContactCreateView,
                    # Payment views
                    PaymentCreateView, PaymentListView, PaymentUpdateView,
                    # Delivery views
                    DeliveryCreateView, DeliveryUpdateView, DeliveryListView,
                    # Vendor self-registration
                    VendorRegisterView, VendorDashboardView, VendorApprovalListView)

urlpatterns = [
    path('', PRListView.as_view(), name='prs-home'),
    path('dashboard/', dashboard_redirect, name='dashboard'),
    path('user/<str:username>', UserPRListView.as_view(), name='user-prs'),
    path('pr/<int:pk>/', PRDetailView.as_view(), name='pr-detail'),
    path('pr/new/', PRCreateView.as_view(), name='pr-create'),
    path('pr/<int:pk>/update/', PRUpdateView.as_view(), name='pr-update'),
    path('pr/<int:pk>/approve/', PRApproveView.as_view(), name='pr-approve'),
    path('pr/<int:pk>/reject/', PRRejectView.as_view(), name='pr-reject'),
    path('pr/<int:pk>/delete/', PRDeleteView.as_view(), name='pr-delete'),
    path('categories/', CategoryListView.as_view(), name='pr-categories'),
    path('buyers/', BuyerListView.as_view(), name='buyers'),
    path('dashboard/buyer/', BuyerDashboardView.as_view(), name='buyer-dashboard'),
    path('dashboard/requester/', RequesterDashboardView.as_view(), name='requester-dashboard'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('archive/', ArchivePRListView.as_view(), name='pr-archive'),
    path('search/', SearchView.as_view(), name='pr-search'),
    
    # Vendor URLs
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('vendors/new/', VendorCreateView.as_view(), name='vendor-create'),
    path('vendors/<int:pk>/update/', VendorUpdateView.as_view(), name='vendor-update'),
    path('vendors/<int:pk>/delete/', VendorDeleteView.as_view(), name='vendor-delete'),
    path('vendors/contact/new/', VendorContactCreateView.as_view(), name='vendor-contact-create'),
    
    # Vendor Self-Registration
    path('vendor/register/', VendorRegisterView.as_view(), name='vendor-register'),
    path('vendor/dashboard/', VendorDashboardView.as_view(), name='vendor-dashboard'),
    path('vendor/approvals/', VendorApprovalListView.as_view(), name='vendor-approval-list'),
    path('vendor/<int:pk>/approve/', views.approve_vendor, name='vendor-approve'),
    path('vendor/<int:pk>/reject/', views.reject_vendor, name='vendor-reject'),
    
    # Payment URLs
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/new/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/update/', PaymentUpdateView.as_view(), name='payment-update'),
    
    # Delivery URLs
    path('deliveries/', DeliveryListView.as_view(), name='delivery-list'),
    path('deliveries/new/', DeliveryCreateView.as_view(), name='delivery-create'),
    path('deliveries/<int:pk>/update/', DeliveryUpdateView.as_view(), name='delivery-update'),
    
    # AJAX URLs
    path('api/get-item-types/', views.get_item_types, name='get-item-types'),
    path('api/get-pr-vendor/', views.get_pr_vendor, name='get-pr-vendor'),

    # Requester payment & tracking
    path('pr/<int:pk>/payment/', views.pr_payment, name='pr-payment'),
    path('pr/<int:pk>/tracking/', views.pr_tracking, name='pr-tracking'),
    path('pr/<int:pk>/tracking/status/', views.pr_tracking_status, name='pr-tracking-status'),

    # Vendor profile & shipping
    path('vendor/profile/edit/', views.vendor_profile_edit, name='vendor-profile-edit'),
    path('pr/<int:pk>/ship/', views.vendor_ship_order, name='vendor-ship-order'),
]
