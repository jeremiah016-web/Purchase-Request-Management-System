# 🛒 Purchase Request Management System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-6.0.2-green?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-Database-lightgrey?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/Bootstrap-4.0-purple?style=for-the-badge&logo=bootstrap&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
</p>

<p align="center">
  A full-stack web application built with <strong>Django</strong> to automate and streamline the procurement workflow of an organization.<br>
  Manages the complete purchase request lifecycle — from creation to vendor quotation, buyer approval, online payment, and real-time delivery tracking.
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [User Roles](#user-roles)
- [Workflow](#workflow)
- [Quick Start](#quick-start)
- [Demo Credentials](#demo-credentials)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [License](#license)

---

## 🔍 Overview

The **Purchase Request Management System** is a centralized digital platform that replaces manual, paper-based procurement processes. It provides role-specific dashboards for all stakeholders — requesters, buyers, vendors, and administrators — enabling transparent, trackable, and efficient procurement.

Built as a final year project at **College of Engineering Poonjar**, Kerala.

---

## ✨ Features

### Core
- 🛍️ **E-commerce style PR creation** — 3-step wizard: browse categories → select item type → fill details
- 📋 **Purchase Request lifecycle** — Open → Pending → Approval → Paid → In Transit → Delivered → Closed
- 👥 **Role-based access control** — 4 distinct roles with dedicated dashboards
- 🔍 **Search & filter** — search PRs by number, category, status

### Vendor Management
- 🏪 **Vendor registration & approval** — admin approves vendors before they can quote
- 💬 **Multi-vendor quotation** — multiple vendors compete; buyer selects the best
- 🏦 **Vendor payment profile** — bank account, IFSC code, UPI ID management
- 📦 **Ship order workflow** — vendor enters tracking number and carrier after payment

### Payment & Tracking
- 💳 **Online payment** — UPI, Credit/Debit Card, Net Banking, Wallet
- 📍 **Real-time delivery tracking** — AJAX polling every 10 seconds, live status updates
- 🔔 **Payment confirmation** — auto-generated transaction ID on successful payment
- 📬 **Delivery address** — requester provides address at payment time

### Admin & Auth
- 🔐 **Google OAuth 2.0** — social login support
- 🛡️ **Django Admin Panel** — full system control for admins
- 📊 **Statistics dashboards** — counts, totals, status summaries per role

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.14, Django 6.0.2 |
| Database | SQLite (development), PostgreSQL (production-ready) |
| Frontend | Bootstrap 4, jQuery 3, JavaScript (ES6) |
| Authentication | django-allauth, Google OAuth 2.0 |
| Forms | django-crispy-forms, crispy-bootstrap4 |
| Icons | Font Awesome 5.15 |
| Fonts | Google Fonts — Inter |
| Image Processing | Pillow 12.1.1 |

---

## 👤 User Roles

| Role | Capabilities |
|------|-------------|
| **Admin** | Full system access, vendor approvals, user management, Django admin panel |
| **Buyer** | Review all PRs, assign vendors, approve quotations, update delivery status |
| **Requester** | Create PRs, approve quotations, pay online, track delivery in real time |
| **Vendor** | Submit quotations, manage profile & payment details, ship orders |

---

## 🔄 Workflow

```
Requester creates PR (e-commerce style wizard)
          ↓
Vendor submits quotation (price + notes)
          ↓
Buyer reviews quotations → selects vendor → approves final price
          ↓
Requester approves quotation → pays online (UPI / Card / Net Banking)
          ↓
Vendor receives payment notification → enters tracking details → ships
          ↓
Requester tracks delivery in real time (auto-updates every 10s)
          ↓
Item delivered → PR closed
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/jeremiah016-web/Purchase-Request-Management-System.git
cd Purchase-Request-Management-System/django_project

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env — add your SECRET_KEY and email settings

# 5. Run database migrations
python manage.py migrate

# 6. Create all demo users (9 accounts across all roles)
python manage.py create_demo_users

# 7. Start the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## 🔑 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `demo_admin` | `Admin@1234` |
| Buyer | `demo_buyer` | `Buyer@1234` |
| Requester | `demo_requester` | `Requester@1234` |
| Vendor — IT | `vendor_it` | `InfoTech@1234` |
| Vendor — Construction | `vendor_construction` | `Construction@1234` |
| Vendor — Consulting | `vendor_consulting` | `Consulting@1234` |
| Vendor — Facility Mgmt | `vendor_facility` | `Facility@1234` |
| Vendor — General Goods | `vendor_general` | `General@1234` |
| Vendor — Office Supplies | `vendor_office` | `Office@1234` |

> Each vendor account is pre-approved and linked to its specific category.

---

## 📁 Project Structure

```
Purchase-Request-Management-System/
├── django_project/
│   ├── django_project/         # Settings, URLs, WSGI/ASGI
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── prs/                    # Main procurement app
│   │   ├── models.py           # PR, Vendor, Payment, Delivery, VendorQuotation
│   │   ├── views.py            # All views + AJAX endpoints
│   │   ├── urls.py             # URL routing (25+ routes)
│   │   ├── admin.py            # Django admin registration
│   │   ├── templates/prs/      # All HTML templates
│   │   ├── static/prs/         # CSS — new-design.css
│   │   └── management/
│   │       └── commands/
│   │           └── create_demo_users.py
│   ├── users/                  # Auth & profile management
│   │   ├── models.py           # Profile with role field
│   │   ├── views.py            # Register, login, profile
│   │   ├── forms.py            # UserRegistrationForm
│   │   ├── mixins.py           # RoleRequiredMixin
│   │   └── templates/users/
│   ├── media/                  # Uploaded files (gitignored)
│   ├── requirements.txt
│   └── .env.example
├── .gitignore
└── README.md
```

---

## 🗄️ Database Models

| Model | Description |
|-------|-------------|
| `PR` | Purchase request — full lifecycle (28 fields) |
| `Vendor` | Vendor profile with payment details (23 fields) |
| `VendorQuotation` | Vendor price quotes per PR |
| `Payment` | Payment transaction records |
| `Delivery` | Shipment tracking details |
| `VendorContact` | Communication log with vendors |
| `Profile` | Extended user with role (admin/buyer/requester/vendor) |

---

## 📸 Screenshots

| Screen | Description |
|--------|-------------|
| Landing Page | Public home with features and contact info |
| Requester Dashboard | PR list with payment status and Pay/Track buttons |
| PR Creation Step 1 | Category cards grid (e-commerce style) |
| PR Creation Step 2 | Item type grid with icons |
| PR Creation Step 3 | Details form with selected category badge |
| Payment Page | Order summary + UPI/Card/NetBanking/Wallet |
| Tracking Page | Live timeline with real-time status updates |
| Vendor Dashboard | Ready-to-ship orders, payment account, available PRs |
| Ship Order | Tracking number, carrier, expected delivery date |
| Admin Dashboard | System-wide stats, recent PRs, vendor approvals |

---

## 📦 Requirements

```
Django==6.0.2
Pillow==12.1.1
django-crispy-forms==2.5
crispy-bootstrap4==2025.6
django-allauth==65.14.3
python-dotenv==1.2.2
```

---

## 🏫 About

**Developer:** Jeremiah George
**Institution:** College of Engineering Poonjar
**Location:** Poonjar, Kottayam, Kerala – 686582
**Contact:** info@cepoonjar.ac.in | +91 4828 278278

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License — Copyright (c) 2025 Jeremiah George
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software.
```
