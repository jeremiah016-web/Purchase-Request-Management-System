# Purchase Request Management System

> A modern, enterprise-grade web application for managing procurement workflows with integrated payment processing, delivery tracking, and automated notifications.

[![Django](https://img.shields.io/badge/Django-6.0.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()

---

## 🚀 Features

### Core Functionality
- ✅ **Purchase Request Management** - Create, track, and manage purchase requests
- ✅ **Vendor Management** - Comprehensive vendor profiles and quotation system
- ✅ **Role-Based Access Control** - Admin, Buyer, Requester, and Vendor roles
- ✅ **Multi-Level Approval Workflow** - Configurable approval thresholds
- ✅ **Dashboard System** - Role-specific dashboards with real-time statistics

### Enterprise Features
- 💳 **Payment Gateway Integration** - Stripe and PayPal support
- 📦 **Real-Time Delivery Tracking** - FedEx, UPS, DHL, USPS integration
- 📧 **Email Notifications** - Automated alerts for all major events
- 📄 **Invoice Generation** - Professional PDF invoices
- 🔐 **Security** - CSRF protection, SQL injection prevention, XSS protection

### Modern UI/UX
- 🎨 **Beautiful Design** - Gradient colors, smooth animations, modern typography
- 📱 **Responsive** - Mobile-first design, works on all devices
- ⚡ **Fast** - Optimized performance, lazy loading, efficient queries
- ♿ **Accessible** - WCAG compliant, keyboard navigation, screen reader support

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Purchase Request
![PR Detail](docs/screenshots/pr-detail.png)

### Vendor Management
![Vendors](docs/screenshots/vendors.png)

---

## 🛠️ Technology Stack

**Backend:**
- Django 6.0.2
- Python 3.14
- SQLite (Development) / PostgreSQL (Production)

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 4
- Font Awesome 5
- Google Fonts (Inter)

**Integrations:**
- Stripe API
- PayPal API
- Carrier APIs (FedEx, UPS, DHL, USPS)
- SMTP Email

**Libraries:**
- django-crispy-forms
- django-allauth
- reportlab
- requests
- python-dotenv

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/jeremiah016-web/Purchase-Request-Management-System.git

# Navigate to project directory
cd Purchase-Request-Management-System/django_project

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Visit http://localhost:8000 to see the application.

---

## 📚 Documentation

- **[Installation Guide](django_project/INSTALLATION.md)** - Detailed setup instructions
- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[Payment & Tracking Guide](PAYMENT_TRACKING_GUIDE.md)** - Enterprise features documentation
- **[UI/UX Guide](UI_UX_GUIDE.md)** - Design system and components
- **[Features Summary](FEATURES_SUMMARY.md)** - Complete feature list
- **[Project Report](PROJECT_REPORT.md)** - Comprehensive project documentation
- **[UML Diagrams](UML_DIAGRAMS.md)** - System architecture diagrams

---

## 👥 User Roles

### 🔑 Admin
- Full system access
- User and vendor management
- System configuration
- Analytics and reporting

### 💼 Buyer
- Review and approve purchase requests
- Assign vendors
- Process payments
- Manage deliveries

### 📝 Requester
- Create purchase requests
- Track request status
- Receive notifications
- View delivery updates

### 🏢 Vendor
- View available requests
- Submit quotations
- Update delivery status
- Receive payment notifications

---

## 🔄 Workflow

```
1. Requester creates PR → Status: Open
2. Buyer reviews PR → Status: Pending
3. Vendors submit quotations
4. Buyer selects vendor & approves price → Status: Approval
5. Payment approval workflow (if required)
6. Payment processed → Invoice generated
7. Vendor ships items → Tracking activated
8. Real-time delivery updates
9. Delivery completed
10. PR closed → Status: Closed
```

---

## 🎨 UI/UX Highlights

### Design System
- **Color Palette**: Purple-blue gradient (#667eea → #764ba2)
- **Typography**: Inter font family
- **Components**: Modern cards, buttons, forms, tables
- **Animations**: Smooth transitions, hover effects, slide-ins

### Key Features
- Gradient backgrounds
- Rounded corners (12px)
- Box shadows for depth
- Hover lift effects
- Responsive grid layouts
- Mobile-optimized

---

## 🔐 Security

- Role-based access control (RBAC)
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure password hashing (PBKDF2)
- Session management
- API key encryption
- HTTPS support

---

## 📊 Statistics

- **Lines of Code**: 15,000+
- **Database Models**: 11
- **Views**: 30+
- **Templates**: 25+
- **API Integrations**: 6
- **Notification Types**: 8+
- **User Roles**: 4
- **Payment Methods**: 5

---

## 🚀 Deployment

### Supported Platforms
- Heroku
- Railway
- PythonAnywhere
- DigitalOcean
- AWS Elastic Beanstalk
- Render

### Production Checklist
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up PostgreSQL database
- [ ] Configure environment variables
- [ ] Collect static files
- [ ] Set up HTTPS
- [ ] Configure email settings
- [ ] Set up backup strategy

---

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Check system
python manage.py check

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📈 Future Enhancements

- [ ] Mobile applications (iOS & Android)
- [ ] AI-powered vendor selection
- [ ] Advanced analytics dashboard
- [ ] ERP system integration
- [ ] Real-time collaboration
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Advanced reporting

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is proprietary software. All rights reserved.

---

## 👨‍💻 Author

**Jeremiah George**
- Email: jeremiahgeorge016@gmail.com
- GitHub: [@jeremiah016-web](https://github.com/jeremiah016-web)

---

## 🙏 Acknowledgments

- Django Software Foundation
- Bootstrap Team
- Font Awesome
- Google Fonts
- Stripe & PayPal Developer Teams
- Open Source Community

---

## 📞 Support

For support, email jeremiahgeorge016@gmail.com or open an issue on GitHub.

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ by Jeremiah George**
