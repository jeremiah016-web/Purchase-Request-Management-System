from django.shortcuts import render, get_object_or_404, redirect
from .models import PR, Vendor, VendorContact, Payment, Delivery
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from users.mixins import RoleRequiredMixin, AdminRequiredMixin, BuyerRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_redirect(request):
    """Redirect users to their role-specific dashboard"""
    if hasattr(request.user, 'profile'):
        if request.user.profile.is_admin():
            return redirect('admin-dashboard')
        elif request.user.profile.is_buyer():
            return redirect('buyer-dashboard')
        elif request.user.profile.is_vendor():
            return redirect('vendor-dashboard')
        else:
            return redirect('requester-dashboard')
    return redirect('requester-dashboard')

### Search

class SearchView(ListView):
    model = PR
    template_name = 'prs/search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
       result = super(SearchView, self).get_queryset()
       query = self.request.GET.get('search')
       if query:
          postresult = PR.objects.filter(pr_number=query)
          result = postresult
       else:
           result = None
       return result

### Control

class CategoryListView(ListView):
    model = PR
    template_name = 'prs/categories.html'
    context_object_name = 'prs'

class BuyerListView(LoginRequiredMixin, BuyerRequiredMixin, ListView):
    model = User
    template_name = 'prs/buyers.html'
    context_object_name = 'buyers'

class BuyerDashboardView(LoginRequiredMixin, BuyerRequiredMixin, ListView):
    """Dashboard for buyers to see PRs that need their attention"""
    model = PR
    template_name = 'prs/buyer_dashboard.html'
    context_object_name = 'prs'
    ordering = ['-date_posted']
    
    def get_queryset(self):
        # Show PRs that are Open or Pending (need buyer action)
        return PR.objects.filter(
            Q(status='Open') | Q(status='Pending')
        ).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add statistics
        context['open_count'] = PR.objects.filter(status='Open').count()
        context['pending_count'] = PR.objects.filter(status='Pending').count()
        context['approval_count'] = PR.objects.filter(status='Approval').count()
        context['on_hold_count'] = PR.objects.filter(status='On Hold').count()
        return context

class RequesterDashboardView(LoginRequiredMixin, ListView):
    """Dashboard for requesters to see their PRs"""
    model = PR
    template_name = 'prs/requester_dashboard.html'
    context_object_name = 'prs'
    ordering = ['-date_posted']
    
    def get_queryset(self):
        # Show only user's own PRs
        return PR.objects.filter(author=self.request.user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_prs = PR.objects.filter(author=self.request.user)
        # Add statistics for user's PRs
        context['my_open_count'] = user_prs.filter(status='Open').count()
        context['my_pending_count'] = user_prs.filter(status='Pending').count()
        context['my_approved_count'] = user_prs.filter(status='Approval').count()
        context['my_done_count'] = user_prs.filter(status='Done').count()
        context['my_total_count'] = user_prs.count()
        return context

class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Dashboard for admins with full system overview"""
    model = PR
    template_name = 'prs/admin_dashboard.html'
    context_object_name = 'prs'
    ordering = ['-date_posted']
    
    def get_queryset(self):
        # Show all PRs
        return PR.objects.all().order_by('-date_posted')[:20]  # Latest 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth.models import User
        
        # System-wide statistics
        context['total_prs'] = PR.objects.count()
        context['open_count'] = PR.objects.filter(status='Open').count()
        context['pending_count'] = PR.objects.filter(status='Pending').count()
        context['approval_count'] = PR.objects.filter(status='Approval').count()
        context['done_count'] = PR.objects.filter(status='Done').count()
        context['closed_count'] = PR.objects.filter(status='Closed').count()
        context['on_hold_count'] = PR.objects.filter(status='On Hold').count()
        
        # User statistics
        context['total_users'] = User.objects.count()
        context['total_requesters'] = User.objects.filter(profile__role='requester').count()
        context['total_buyers'] = User.objects.filter(profile__role='buyer').count()
        context['total_admins'] = User.objects.filter(profile__role='admin').count()
        
        # Recent activity
        context['recent_prs'] = PR.objects.all().order_by('-date_posted')[:5]
        
        return context

### PR List

class PRListView(ListView):
    model = PR
    template_name = 'prs/home.html'
    context_object_name = 'prs'
    ordering = ['-date_posted']
    #paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to their role-specific dashboard
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile'):
                if request.user.profile.is_admin():
                    return redirect('admin-dashboard')
                elif request.user.profile.is_buyer():
                    return redirect('buyer-dashboard')
                else:
                    return redirect('requester-dashboard')
        # For non-authenticated users, show the home page
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return PR.objects.filter(Q(status="Approval") | Q(status="Done") | Q(status="On Hold") | Q(status="Pending") | Q(status="Open")).order_by('-date_posted')

class UserPRListView(ListView):
    model = PR
    template_name = 'prs/user_prs.html'
    context_object_name = 'prs'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return PR.objects.filter(author=user).order_by('-date_posted')

class ArchivePRListView(ListView):
    model = PR
    template_name = 'prs/prs_archive.html'
    context_object_name = 'prs'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        #status = get_object_or_404(PR, status=self.kwargs.get('closed'))
        return PR.objects.filter(status='Closed').order_by('-date_posted')


##

class PRDetailView(DetailView):
    model = PR
    template_name = 'prs/pr_detail.html'
    context_object_name = 'pr'

class PRCreateView(LoginRequiredMixin, CreateView):
    model = PR
    template_name = 'prs/pr_new.html'
    fields = ['pr_number', 'category', 'item_type', 'items_description', 'quantity', 'specifications', 'description']

    def dispatch(self, request, *args, **kwargs):
        # Only requesters can create PRs
        if hasattr(request.user, 'profile'):
            if not request.user.profile.is_requester():
                from django.contrib import messages
                messages.error(request, 'Only requesters can create purchase requests.')
                return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Add labels and help text
        if 'item_type' in form.fields:
            form.fields['item_type'].label = 'Item Type'
            form.fields['item_type'].help_text = 'What type of item or service do you need?'
            form.fields['item_type'].required = True
        
        if 'items_description' in form.fields:
            form.fields['items_description'].label = 'Items Description'
            form.fields['items_description'].help_text = 'Provide detailed description of what you need'
            form.fields['items_description'].required = True
        
        if 'quantity' in form.fields:
            form.fields['quantity'].label = 'Quantity'
            form.fields['quantity'].help_text = 'How many do you need? (e.g., 10 units, 5 boxes, 100 pieces)'
            form.fields['quantity'].required = True
        
        if 'specifications' in form.fields:
            form.fields['specifications'].label = 'Specifications (Optional)'
            form.fields['specifications'].help_text = 'Technical specifications, dimensions, colors, etc.'
            form.fields['specifications'].required = False
        
        if 'description' in form.fields:
            form.fields['description'].label = 'Additional Notes (Optional)'
            form.fields['description'].help_text = 'Any other information that might be helpful'
            form.fields['description'].required = False
        
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Set status to 'Open' for requesters
        form.instance.status = 'Open'
        # Price will be set by vendor later
        form.instance.total = 0.00
        return super().form_valid(form)


class PRUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PR
    template_name = 'prs/pr_update.html'
    fields = ['status', 'category', 'item_type', 'items_description', 'quantity', 'specifications', 'description', 
              'vendor', 'estimated_price', 'quotation_notes', 'total', 
              'vendor_name', 'vendor_contact', 'payment_status', 'payment_date', 'payment_notes', 'delivery_status']  # All fields
    
    def get_form(self, form_class=None):
        """Customize form fields based on user role"""
        form = super().get_form(form_class)
        pr = self.get_object()
        user = self.request.user
        
        # Add labels and help text
        if 'item_type' in form.fields:
            form.fields['item_type'].label = 'Item Type'
        if 'items_description' in form.fields:
            form.fields['items_description'].label = 'Items Description'
        if 'quantity' in form.fields:
            form.fields['quantity'].label = 'Quantity'
        if 'specifications' in form.fields:
            form.fields['specifications'].label = 'Specifications'
        if 'estimated_price' in form.fields:
            form.fields['estimated_price'].label = 'Estimated Price (Quotation)'
            form.fields['estimated_price'].help_text = 'Vendor: Enter your estimated price'
            form.fields['estimated_price'].required = False
        if 'quotation_notes' in form.fields:
            form.fields['quotation_notes'].label = 'Quotation Notes'
            form.fields['quotation_notes'].help_text = 'Vendor: Provide price breakdown and details'
            form.fields['quotation_notes'].required = False
        if 'total' in form.fields:
            form.fields['total'].label = 'Approved Price'
            form.fields['total'].help_text = 'Buyer: Approve vendor quotation'
            form.fields['total'].required = False
        if 'vendor' in form.fields:
            form.fields['vendor'].label = 'Assign Vendor'
            form.fields['vendor'].help_text = 'Select a vendor from the approved list'
            form.fields['vendor'].required = False
            # Only show approved vendors
            form.fields['vendor'].queryset = Vendor.objects.filter(is_approved=True, status='Active')
        if 'payment_status' in form.fields:
            form.fields['payment_status'].required = False
        if 'payment_date' in form.fields:
            form.fields['payment_date'].widget.attrs['type'] = 'date'
            form.fields['payment_date'].required = False
        if 'payment_notes' in form.fields:
            form.fields['payment_notes'].required = False
        if 'delivery_status' in form.fields:
            form.fields['delivery_status'].label = 'Delivery Status'
            form.fields['delivery_status'].required = False
        
        # Remove fields based on role
        if hasattr(user, 'profile'):
            if user.profile.is_admin():
                # Admin can edit everything
                pass
            elif user.profile.is_buyer():
                # Buyer can assign vendor, approve quotation, update status, manage payment/delivery
                # Remove item detail fields (requester only)
                for field in ['item_type', 'items_description', 'quantity', 'specifications']:
                    if field in form.fields:
                        del form.fields[field]
                # Remove vendor quotation fields (vendor only)
                if 'estimated_price' in form.fields:
                    del form.fields['estimated_price']
                if 'quotation_notes' in form.fields:
                    del form.fields['quotation_notes']
                # Buyers can approve the final price and manage delivery/payment
                if 'total' in form.fields:
                    form.fields['total'].help_text = 'Approve the vendor\'s quotation by entering the final price'
            elif user.profile.is_vendor():
                # Vendor can submit quotation only
                # Remove all fields except quotation fields
                for field in ['status', 'category', 'item_type', 'items_description', 'quantity', 'specifications',
                             'vendor', 'total', 'vendor_name', 'vendor_contact', 'payment_status', 'payment_date', 
                             'payment_notes', 'delivery_status']:
                    if field in form.fields:
                        del form.fields[field]
                # Vendor can only submit quotation
                if 'estimated_price' in form.fields:
                    form.fields['estimated_price'].help_text = 'Enter your estimated price for this request'
                    form.fields['estimated_price'].required = True
                if 'quotation_notes' in form.fields:
                    form.fields['quotation_notes'].help_text = 'Provide detailed price breakdown and any notes'
            else:
                # Requester can edit item details when PR is Open
                # Remove vendor, quotation, and payment fields
                for field in ['vendor', 'estimated_price', 'quotation_notes', 'total',
                             'vendor_name', 'vendor_contact', 'payment_status', 'payment_date', 'payment_notes', 'delivery_status']:
                    if field in form.fields:
                        del form.fields[field]
                
                if 'status' in form.fields:
                    del form.fields[field]
                    
                if pr.status != 'Open':
                    # If not Open, make all fields readonly
                    for field in form.fields:
                        form.fields[field].widget.attrs['readonly'] = True
                        form.fields[field].help_text = 'PR is being processed - cannot edit'
        
        return form

    def form_valid(self, form):
        user = self.request.user
        pr = self.get_object()
        
        # Handle vendor quotation submission
        if hasattr(user, 'profile') and user.profile.is_vendor():
            try:
                vendor = Vendor.objects.get(user=user)
                # Create or update VendorQuotation
                from .models import VendorQuotation
                quotation, created = VendorQuotation.objects.update_or_create(
                    pr=pr,
                    vendor=vendor,
                    defaults={
                        'estimated_price': form.cleaned_data.get('estimated_price'),
                        'quotation_notes': form.cleaned_data.get('quotation_notes', ''),
                        'quotation_date': timezone.now()
                    }
                )
                
                # Also update legacy fields for backward compatibility
                form.instance.quotation_date = timezone.now()
                form.instance.quotation_submitted_by = user
                
                # If vendor is not assigned yet, assign them when they submit quotation
                if not pr.vendor:
                    form.instance.vendor = vendor
                    
                from django.contrib import messages
                if created:
                    messages.success(self.request, 'Your quotation has been submitted successfully!')
                else:
                    messages.success(self.request, 'Your quotation has been updated successfully!')
            except Vendor.DoesNotExist:
                pass
        
        # Handle buyer price approval and vendor selection
        if hasattr(user, 'profile') and user.profile.is_buyer():
            # If buyer selects a vendor and approves price
            if form.cleaned_data.get('vendor'):
                selected_vendor = form.cleaned_data.get('vendor')
                
                # Mark the selected vendor's quotation as selected
                from .models import VendorQuotation
                VendorQuotation.objects.filter(pr=pr).update(is_selected=False)  # Deselect all
                quotation = VendorQuotation.objects.filter(pr=pr, vendor=selected_vendor).first()
                if quotation:
                    quotation.is_selected = True
                    quotation.selected_by = user
                    quotation.selected_date = timezone.now()
                    quotation.save()
                    
                    # Set the approved price from the selected quotation
                    if not form.cleaned_data.get('total') or form.cleaned_data.get('total') == 0:
                        form.instance.total = quotation.estimated_price
                
                # Approve the price
                if form.cleaned_data.get('total') and form.cleaned_data['total'] > 0:
                    if not form.instance.price_approved:
                        form.instance.price_approved = True
                        form.instance.price_approved_by = user
                        form.instance.price_approved_date = timezone.now()
                        # Update status to Approval when price is approved
                        if form.instance.status in ['Open', 'Pending']:
                            form.instance.status = 'Approval'
                        
                        from django.contrib import messages
                        messages.success(self.request, f'Vendor {selected_vendor.name} has been selected and price approved!')
        
        return super().form_valid(form)

    def test_func(self):
        pr = self.get_object()
        user = self.request.user
        
        # Admin can update anything
        if hasattr(user, 'profile') and user.profile.is_admin():
            return True
        
        # Buyer can update any PR
        if hasattr(user, 'profile') and user.profile.is_buyer():
            return True
        
        # Vendor can update PRs in their category (to submit quotations)
        if hasattr(user, 'profile') and user.profile.is_vendor():
            try:
                vendor = Vendor.objects.get(user=user)
                # Check if PR category matches vendor's categories
                vendor_categories = [cat.strip() for cat in vendor.categories.split(',')] if vendor.categories else []
                return pr.category in vendor_categories
            except Vendor.DoesNotExist:
                return False
        
        # Requester can only update their own PRs
        if user == pr.author:
            return True
        
        return False

class PRApproveView(LoginRequiredMixin, BuyerRequiredMixin, UpdateView):
    """Quick approve action for buyers"""
    model = PR
    template_name = 'prs/pr_approve.html'
    fields = ['description']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'approve'
        return context
    
    def form_valid(self, form):
        # Set status to Approval
        form.instance.status = 'Approval'
        # Add approval note
        if form.cleaned_data.get('description'):
            form.instance.description += f"\n\n[APPROVED by {self.request.user.username}]: {form.cleaned_data['description']}"
        else:
            form.instance.description += f"\n\n[APPROVED by {self.request.user.username}]"
        return super().form_valid(form)

class PRRejectView(LoginRequiredMixin, BuyerRequiredMixin, UpdateView):
    """Quick reject action for buyers"""
    model = PR
    template_name = 'prs/pr_approve.html'
    fields = ['description']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'reject'
        return context
    
    def form_valid(self, form):
        # Set status to Closed
        form.instance.status = 'Closed'
        # Add rejection note
        if form.cleaned_data.get('description'):
            form.instance.description += f"\n\n[REJECTED by {self.request.user.username}]: {form.cleaned_data['description']}"
        else:
            form.instance.description += f"\n\n[REJECTED by {self.request.user.username}]"
        return super().form_valid(form)

class PRDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PR
    template_name = 'prs/pr_delete.html'
    success_url = '/'

    def test_func(self):
        pr = self.get_object()
        user = self.request.user
        
        # Admin can delete anything
        if hasattr(user, 'profile') and user.profile.is_admin():
            return True
        
        # Requester can delete their own PRs if status is 'Open'
        if user == pr.author and pr.status == 'Open':
            return True
        
        return False


# ============================================
# VENDOR MANAGEMENT VIEWS
# ============================================

class VendorListView(LoginRequiredMixin, BuyerRequiredMixin, ListView):
    """List all vendors - accessible by buyers and admins"""
    model = Vendor
    template_name = 'prs/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Vendor.objects.all()
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(contact_person__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset


class VendorDetailView(LoginRequiredMixin, BuyerRequiredMixin, DetailView):
    """View vendor details"""
    model = Vendor
    template_name = 'prs/vendor_detail.html'
    context_object_name = 'vendor'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.get_object()
        context['prs'] = vendor.pr_set.all().order_by('-date_posted')
        context['contacts'] = vendor.contacts.all()[:10]
        context['payments'] = Payment.objects.filter(vendor=vendor).order_by('-payment_date')[:10]
        context['deliveries'] = Delivery.objects.filter(vendor=vendor).order_by('-created_at')[:10]
        return context


class VendorCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Create new vendor - Admin only (vendors should self-register)"""
    model = Vendor
    template_name = 'prs/vendor_form.html'
    fields = ['name', 'contact_person', 'email', 'phone', 'address', 'website', 
              'tax_id', 'bank_account', 'payment_terms', 'categories', 'status', 'notes']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Make categories field a multiple select
        from django import forms
        from .models import category_choice
        
        form.fields['categories'] = forms.MultipleChoiceField(
            choices=category_choice,
            widget=forms.CheckboxSelectMultiple,
            required=True,
            help_text="Select all categories this vendor can serve"
        )
        
        return form
    
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.is_approved = True  # Admin-created vendors are auto-approved
        form.instance.approved_by = self.request.user
        form.instance.approved_date = timezone.now()
        
        # Convert list of categories to comma-separated string
        categories_list = form.cleaned_data.get('categories', [])
        form.instance.categories = ', '.join(categories_list)
        
        return super().form_valid(form)


class VendorUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """Update vendor information - Admin only"""
    model = Vendor
    template_name = 'prs/vendor_form.html'
    fields = ['name', 'contact_person', 'email', 'phone', 'address', 'website', 
              'tax_id', 'bank_account', 'payment_terms', 'categories', 'status', 'rating', 'notes']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Make categories field a multiple select
        from django import forms
        from .models import category_choice
        
        # Get current categories
        current_categories = []
        if self.object.categories:
            current_categories = [cat.strip() for cat in self.object.categories.split(',')]
        
        form.fields['categories'] = forms.MultipleChoiceField(
            choices=category_choice,
            widget=forms.CheckboxSelectMultiple,
            required=True,
            initial=current_categories,
            help_text="Select all categories this vendor can serve"
        )
        
        return form
    
    def form_valid(self, form):
        # Convert list of categories to comma-separated string
        categories_list = form.cleaned_data.get('categories', [])
        form.instance.categories = ', '.join(categories_list)
        
        return super().form_valid(form)


class VendorDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """Delete vendor - admin only"""
    model = Vendor
    template_name = 'prs/vendor_confirm_delete.html'
    success_url = '/vendors/'


# ============================================
# VENDOR CONTACT VIEWS
# ============================================

class VendorContactCreateView(LoginRequiredMixin, BuyerRequiredMixin, CreateView):
    """Log contact with vendor"""
    model = VendorContact
    template_name = 'prs/vendor_contact_form.html'
    fields = ['vendor', 'pr', 'contact_type', 'subject', 'message', 'response', 'follow_up_date']
    
    def form_valid(self, form):
        form.instance.contacted_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('vendor-detail', kwargs={'pk': self.object.vendor.pk})


# ============================================
# PAYMENT VIEWS
# ============================================

class PaymentCreateView(LoginRequiredMixin, BuyerRequiredMixin, CreateView):
    """Record a payment"""
    model = Payment
    template_name = 'prs/payment_form.html'
    fields = ['pr', 'vendor', 'amount', 'payment_method', 'payment_date', 
              'reference_number', 'status', 'notes']
    
    def form_valid(self, form):
        form.instance.processed_by = self.request.user
        # Update PR payment status
        pr = form.instance.pr
        if form.instance.status == 'Paid':
            total_paid = pr.total_paid() + form.instance.amount
            if total_paid >= pr.total:
                pr.payment_status = 'Paid'
            else:
                pr.payment_status = 'Partially Paid'
            pr.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('pr-detail', kwargs={'pk': self.object.pr.pk})


class PaymentListView(LoginRequiredMixin, BuyerRequiredMixin, ListView):
    """List all payments"""
    model = Payment
    template_name = 'prs/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 50
    ordering = ['-payment_date']


class PaymentUpdateView(LoginRequiredMixin, BuyerRequiredMixin, UpdateView):
    """Update payment information"""
    model = Payment
    template_name = 'prs/payment_form.html'
    fields = ['amount', 'payment_method', 'payment_date', 'reference_number', 'status', 'notes']
    
    def get_success_url(self):
        return reverse('pr-detail', kwargs={'pk': self.object.pr.pk})


# ============================================
# DELIVERY TRACKING VIEWS
# ============================================

class DeliveryCreateView(LoginRequiredMixin, BuyerRequiredMixin, CreateView):
    """Create delivery tracking"""
    model = Delivery
    template_name = 'prs/delivery_form.html'
    fields = ['pr', 'vendor', 'tracking_number', 'carrier', 'status', 
              'shipped_date', 'expected_delivery_date', 'actual_delivery_date',
              'delivery_address', 'recipient_name', 'recipient_contact', 'notes']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # Update PR delivery status
        pr = form.instance.pr
        pr.delivery_status = form.instance.status
        pr.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('pr-detail', kwargs={'pk': self.object.pr.pk})


class DeliveryUpdateView(LoginRequiredMixin, BuyerRequiredMixin, UpdateView):
    """Update delivery tracking"""
    model = Delivery
    template_name = 'prs/delivery_form.html'
    fields = ['tracking_number', 'carrier', 'status', 'shipped_date', 
              'expected_delivery_date', 'actual_delivery_date',
              'delivery_address', 'recipient_name', 'recipient_contact', 'notes']
    
    def form_valid(self, form):
        # Update PR delivery status
        pr = form.instance.pr
        pr.delivery_status = form.instance.status
        pr.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('pr-detail', kwargs={'pk': self.object.pr.pk})


class DeliveryListView(LoginRequiredMixin, BuyerRequiredMixin, ListView):
    """List all deliveries"""
    model = Delivery
    template_name = 'prs/delivery_list.html'
    context_object_name = 'deliveries'
    paginate_by = 50
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset



# ============================================
# VENDOR SELF-REGISTRATION VIEWS
# ============================================

class VendorRegisterView(CreateView):
    """Public vendor registration - no login required"""
    model = Vendor
    template_name = 'prs/vendor_register.html'
    fields = ['name', 'contact_person', 'email', 'phone', 'address', 'website', 
              'tax_id', 'bank_account', 'payment_terms', 'categories']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Make categories field a multiple select
        from django import forms
        from .models import category_choice
        
        form.fields['categories'] = forms.MultipleChoiceField(
            choices=category_choice,
            widget=forms.CheckboxSelectMultiple,
            required=True,
            help_text="Select all categories you can serve"
        )
        
        # Update other field properties
        form.fields['name'].help_text = "Your company/business name"
        form.fields['email'].required = True
        form.fields['phone'].required = True
        
        return form
    
    def form_valid(self, form):
        # Check if user is logged in
        if self.request.user.is_authenticated:
            # Link vendor to user account
            form.instance.user = self.request.user
            form.instance.added_by = self.request.user
            # Update user role to vendor
            if hasattr(self.request.user, 'profile'):
                self.request.user.profile.role = 'vendor'
                self.request.user.profile.save()
        
        # Convert list of categories to comma-separated string
        categories_list = form.cleaned_data.get('categories', [])
        form.instance.categories = ', '.join(categories_list)
        
        # Set status to Pending (requires admin approval)
        form.instance.status = 'Pending'
        form.instance.is_approved = False
        
        response = super().form_valid(form)
        
        # Show success message
        from django.contrib import messages
        messages.success(self.request, 'Your vendor registration has been submitted! An admin will review and approve your account.')
        
        return response
    
    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse('vendor-dashboard')
        return reverse('login')


class VendorDashboardView(LoginRequiredMixin, DetailView):
    """Vendor dashboard - shows their vendor profile and orders"""
    model = Vendor
    template_name = 'prs/vendor_dashboard.html'
    context_object_name = 'vendor'
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user has vendor profile
        try:
            Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            # Redirect to registration if no vendor profile
            from django.contrib import messages
            messages.info(request, 'Please complete your vendor registration first.')
            return redirect('vendor-register')
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        # Get vendor profile for current user
        return Vendor.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.get_object()
        
        # Get vendor's categories (comma-separated string to list)
        vendor_categories = [cat.strip() for cat in vendor.categories.split(',')] if vendor.categories else []
        
        # Get PRs in vendor's categories that are Open or Pending (available for quotation)
        available_prs = PR.objects.filter(
            category__in=vendor_categories,
            status__in=['Open', 'Pending']
        ).exclude(
            vendor=vendor  # Exclude already assigned to this vendor
        ).order_by('-date_posted')
        
        # Get vendor's assigned PRs
        context['prs'] = vendor.pr_set.all().order_by('-date_posted')
        context['available_prs'] = available_prs  # PRs vendor can quote on
        context['pending_prs'] = vendor.pr_set.filter(status='Pending').count()
        context['approved_prs'] = vendor.pr_set.filter(status='Approval').count()
        context['total_value'] = sum(pr.total for pr in vendor.pr_set.all())
        
        # Get payments
        context['payments'] = Payment.objects.filter(vendor=vendor).order_by('-payment_date')[:10]
        context['total_paid'] = sum(p.amount for p in Payment.objects.filter(vendor=vendor, status='Paid'))
        
        # Get deliveries
        context['deliveries'] = Delivery.objects.filter(vendor=vendor).order_by('-created_at')[:10]
        context['pending_deliveries'] = Delivery.objects.filter(vendor=vendor, status='In Transit').count()
        
        return context


class VendorApprovalListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Admin view to approve/reject vendor registrations"""
    model = Vendor
    template_name = 'prs/vendor_approval_list.html'
    context_object_name = 'vendors'
    
    def get_queryset(self):
        # Show only pending vendors
        return Vendor.objects.filter(is_approved=False, status='Pending').order_by('-date_added')


@login_required
def approve_vendor(request, pk):
    """Admin approves vendor"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin():
        from django.contrib import messages
        messages.error(request, 'You do not have permission to approve vendors.')
        return redirect('dashboard')
    
    vendor = get_object_or_404(Vendor, pk=pk)
    vendor.is_approved = True
    vendor.status = 'Active'
    vendor.approved_by = request.user
    vendor.approved_date = timezone.now()
    vendor.save()
    
    from django.contrib import messages
    messages.success(request, f'Vendor "{vendor.name}" has been approved!')
    
    return redirect('vendor-approval-list')


@login_required
def reject_vendor(request, pk):
    """Admin rejects vendor"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin():
        from django.contrib import messages
        messages.error(request, 'You do not have permission to reject vendors.')
        return redirect('dashboard')
    
    vendor = get_object_or_404(Vendor, pk=pk)
    vendor.status = 'Inactive'
    vendor.is_approved = False
    vendor.save()
    
    from django.contrib import messages
    messages.warning(request, f'Vendor "{vendor.name}" has been rejected.')
    
    return redirect('vendor-approval-list')



# ============================================
# AJAX VIEWS FOR DYNAMIC DROPDOWNS
# ============================================

from django.http import JsonResponse
from .models import ITEM_TYPE_CHOICES

def get_item_types(request):
    """Return item types for selected category"""
    category = request.GET.get('category', '')
    
    if category in ITEM_TYPE_CHOICES:
        item_types = [{'value': value, 'label': label} for value, label in ITEM_TYPE_CHOICES[category]]
        return JsonResponse({'item_types': item_types})
    
    return JsonResponse({'item_types': []})
