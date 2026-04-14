"""
Management command: python manage.py create_demo_users
Creates demo accounts for every role including one vendor per category.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile
from prs.models import Vendor
from django.utils import timezone

# Non-vendor roles
DEMO_USERS = [
    {
        'username': 'demo_admin',
        'password': 'Admin@1234',
        'email': 'admin@cepoonjar.ac.in',
        'first_name': 'Admin', 'last_name': 'User',
        'role': 'admin', 'is_staff': True, 'is_superuser': True,
    },
    {
        'username': 'demo_buyer',
        'password': 'Buyer@1234',
        'email': 'buyer@cepoonjar.ac.in',
        'first_name': 'Buyer', 'last_name': 'User',
        'role': 'buyer', 'is_staff': False, 'is_superuser': False,
    },
    {
        'username': 'demo_requester',
        'password': 'Requester@1234',
        'email': 'requester@cepoonjar.ac.in',
        'first_name': 'Requester', 'last_name': 'User',
        'role': 'requester', 'is_staff': False, 'is_superuser': False,
    },
]

# One vendor user + vendor profile per category
DEMO_VENDORS = [
    {
        'username': 'vendor_construction',
        'password': 'Construction@1234',
        'email': 'construction@buildpro.in',
        'first_name': 'BuildPro',
        'last_name': 'Constructions',
        'vendor': {
            'name': 'BuildPro Constructions Pvt. Ltd.',
            'contact_person': 'Rajan Nair',
            'email': 'construction@buildpro.in',
            'phone': '+91 9400111001',
            'address': 'NH 183, Ernakulam, Kerala 682001',
            'categories': 'Construction',
            'payment_terms': 'Net 30',
            'rating': 4,
            'notes': 'Specialises in civil construction, steel, cement and building materials.',
        },
    },
    {
        'username': 'vendor_consulting',
        'password': 'Consulting@1234',
        'email': 'consulting@strategix.in',
        'first_name': 'Strategix',
        'last_name': 'Consulting',
        'vendor': {
            'name': 'Strategix Consulting Services',
            'contact_person': 'Priya Menon',
            'email': 'consulting@strategix.in',
            'phone': '+91 9400222002',
            'address': 'Technopark, Thiruvananthapuram, Kerala 695581',
            'categories': 'Consulting',
            'payment_terms': 'Net 15',
            'rating': 5,
            'notes': 'Business, IT, HR and management consulting for educational institutions.',
        },
    },
    {
        'username': 'vendor_facility',
        'password': 'Facility@1234',
        'email': 'facility@cleanserve.in',
        'first_name': 'CleanServe',
        'last_name': 'Facility',
        'vendor': {
            'name': 'CleanServe Facility Management',
            'contact_person': 'Suresh Kumar',
            'email': 'facility@cleanserve.in',
            'phone': '+91 9400333003',
            'address': 'MG Road, Kottayam, Kerala 686001',
            'categories': 'Facility Management',
            'payment_terms': 'Net 30',
            'rating': 4,
            'notes': 'Cleaning, security, HVAC, pest control and building maintenance services.',
        },
    },
    {
        'username': 'vendor_general',
        'password': 'General@1234',
        'email': 'general@supplyhub.in',
        'first_name': 'SupplyHub',
        'last_name': 'General',
        'vendor': {
            'name': 'SupplyHub General Traders',
            'contact_person': 'Anitha George',
            'email': 'general@supplyhub.in',
            'phone': '+91 9400444004',
            'address': 'Baker Junction, Kottayam, Kerala 686001',
            'categories': 'General Goods and Services',
            'payment_terms': 'Advance',
            'rating': 3,
            'notes': 'Furniture, uniforms, catering, courier and general procurement supplies.',
        },
    },
    {
        'username': 'vendor_it',
        'password': 'InfoTech@1234',
        'email': 'it@techzone.in',
        'first_name': 'TechZone',
        'last_name': 'IT',
        'vendor': {
            'name': 'TechZone IT Solutions',
            'contact_person': 'Arun Pillai',
            'email': 'it@techzone.in',
            'phone': '+91 9400555005',
            'address': 'Infopark, Kakkanad, Ernakulam, Kerala 682042',
            'categories': 'Information Technology',
            'payment_terms': 'Net 45',
            'rating': 5,
            'notes': 'Hardware, software, networking, cloud services and IT security solutions.',
        },
    },
    {
        'username': 'vendor_office',
        'password': 'Office@1234',
        'email': 'office@stationmart.in',
        'first_name': 'StationMart',
        'last_name': 'Office',
        'vendor': {
            'name': 'StationMart Office Supplies',
            'contact_person': 'Deepa Thomas',
            'email': 'office@stationmart.in',
            'phone': '+91 9400666006',
            'address': 'Poonjar, Kottayam, Kerala 686582',
            'categories': 'Office Supplies',
            'payment_terms': 'Net 15',
            'rating': 4,
            'notes': 'Paper, stationery, filing, desk accessories and office electronics.',
        },
    },
]


class Command(BaseCommand):
    help = 'Create demo users for every role (admin, buyer, requester, 6 category vendors)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n=== Creating Non-Vendor Demo Users ===\n'))

        for data in DEMO_USERS:
            user, created = User.objects.get_or_create(username=data['username'])
            user.set_password(data['password'])
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.is_staff = data['is_staff']
            user.is_superuser = data['is_superuser']
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = data['role']
            profile.save()
            status = 'created' if created else 'updated'
            self.stdout.write(self.style.SUCCESS(
                f"  [{data['role'].upper():12}]  {data['username']:25} / {data['password']}  ({status})"
            ))

        self.stdout.write(self.style.MIGRATE_HEADING('\n=== Creating Vendor Demo Users ===\n'))

        admin_user = User.objects.get(username='demo_admin')

        for data in DEMO_VENDORS:
            user, created = User.objects.get_or_create(username=data['username'])
            user.set_password(data['password'])
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.is_staff = False
            user.is_superuser = False
            user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = 'vendor'
            profile.save()

            vdata = data['vendor']
            vendor, v_created = Vendor.objects.get_or_create(
                user=user,
                defaults={
                    **vdata,
                    'status': 'Active',
                    'is_approved': True,
                    'added_by': admin_user,
                    'approved_by': admin_user,
                    'approved_date': timezone.now(),
                }
            )
            if not v_created:
                vendor.is_approved = True
                vendor.status = 'Active'
                vendor.name = vdata['name']
                vendor.categories = vdata['categories']
                vendor.save()

            u_status = 'created' if created else 'updated'
            self.stdout.write(self.style.SUCCESS(
                f"  [VENDOR/{vdata['categories']:30}]  {data['username']:25} / {data['password']}  ({u_status})"
            ))

        self.stdout.write(self.style.MIGRATE_HEADING('\n=== All Demo Credentials ===\n'))
        self.stdout.write(f"  {'Role':<35} {'Username':<25} {'Password'}")
        self.stdout.write(f"  {'-'*35} {'-'*25} {'-'*20}")
        for d in DEMO_USERS:
            self.stdout.write(f"  {d['role']:<35} {d['username']:<25} {d['password']}")
        for d in DEMO_VENDORS:
            label = f"vendor ({d['vendor']['categories']})"
            self.stdout.write(f"  {label:<35} {d['username']:<25} {d['password']}")
        self.stdout.write('')
