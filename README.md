# 🚀 StuLance - Academic Freelancing Platform

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/ladroxd/StuLance)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.x-darkgreen.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-brightblue.svg)](#)

**StuLance** is an innovative web platform that allows **Moroccan students** to showcase their skills as freelancers while offering recruiters (companies, startups, individuals) a secure and reliable way to hire qualified talent.

> 💡 **Solving a real problem**: How can students access freelance opportunities adapted to their academic schedule, in a secure environment suited to the Moroccan context?

---

## 📑 Table of Contents

1. [🎯 Project Overview](#-project-overview)
2. [✨ Features](#-features)
3. [🏗️ Architecture](#️-architecture)
4. [⚙️ Tech Stack](#️-tech-stack)
5. [📦 Installation](#-installation)
6. [🔧 Configuration](#-configuration)
7. [🚀 Usage](#-usage)
8. [📁 Project Structure](#-project-structure)
9. [🗄️ Data Models](#️-data-models)
10. [🔌 API Endpoints](#-api-endpoints)
11. [🔐 Security & Authentication](#-security--authentication)
12. [🧪 Tests](#-tests)
13. [🌐 Deployment](#-deployment)
14. [📚 Documentation](#-documentation)

---

## 🎯 Project Overview

### Context & Problem Statement

Freelancing is growing exponentially worldwide. Students in computer science, design, marketing, and management have real skills but lack platforms adapted to their Moroccan academic context.

**Identified problems**:
- ❌ Existing platforms (Upwork, Fiverr) are generic and in English
- ❌ No adaptation to the academic calendar and student constraints
- ❌ No student status verification
- ❌ Complexity for Moroccan users

**The Solution**: **StuLance** — A dedicated, secure platform adapted to the Moroccan academic context.

### Objectives

**General**:
- ✅ Create a web platform allowing students to offer their services
- ✅ Allow recruiters to post missions and hire talent
- ✅ Provide a secure, transparent and academically adapted environment

**Specific**:
- ✅ Profile system with portfolio and skills
- ✅ Search engine and student/recruiter matching
- ✅ Mission tracking and mutual rating system
- ✅ Student status verification via student card
- ✅ Administration back-office for moderation

---

## ✨ Features

### 👤 User & Profile Management

#### Registration & Authentication
```
✅ Secure registration for students and recruiters
✅ Email/password authentication
✅ Secure Django session (CSRF protection)
✅ Automatic profile creation upon registration
```

#### Student Profiles
```
✅ Student card upload for verification
✅ Manual verification by administrator (pending/verified/rejected)
✅ Bio, profile photo, skills (tags)
✅ GitHub and LinkedIn links
✅ Academic information (school, field of study)
✅ Portfolio with completed projects
✅ Average rating and mission statistics
```

#### Recruiter Profiles
```
✅ Client type (Company or Individual)
✅ Company/person name
✅ Bio, profile photo
✅ Website
✅ Average rating
```

### 🎯 Mission Management

#### Publishing Missions
```
✅ Title, detailed description
✅ Budget in MAD (Moroccan Dirham)
✅ Duration in days
✅ Mission category
✅ Required skills
✅ Status: Open → In Progress → Completed → Reviewed
```

#### Search & Filtering
```
✅ Keyword search
✅ Filter by category
✅ Filter by budget (min/max)
✅ Filter by duration
✅ Display open missions only
```

#### Mission Lifecycle
```
Open
  ↓
In Progress (Accepted)
  ↓
Completed
  ↓
Reviewed
```

### 📋 Application System

```
✅ Apply with a cover letter
✅ Status: Pending → Accepted → Rejected
✅ A student can only apply once per mission
✅ Recruiter sees all applicants and their profiles
✅ Acceptance triggers a notification
✅ Automatic rejection of other applicants
✅ Student mission counter updated
```

### 💬 Messaging & Communication

```
✅ Mission-contextualised messaging
✅ Conversation between student and recruiter
✅ Message history
✅ Read/unread marking
✅ New message notifications
✅ Direct link from each mission
```

### 📊 Dashboards

#### Student Dashboard
```
✅ Pending applications
✅ Accepted missions (in_progress)
✅ Completed missions
✅ Average rating received
✅ Total missions completed
✅ Quick access to profile and portfolio
```

#### Recruiter Dashboard
```
✅ Posted missions (open, in_progress, completed)
✅ Applications received per mission
✅ Applicant profiles
✅ Accept/reject buttons
✅ Past mission history
✅ Account management
```

### ⭐ Rating & Review System

```
✅ 1-5 star rating + comment
✅ After mission closure only
✅ Bilateral rating (recruiter → student and vice versa)
✅ Automatic average rating calculation
✅ Reviews displayed on profiles
✅ Unique per pair (mission, reviewer)
```

### 🔔 Notifications

Notification types:
```
✅ New application: Recruiter notified when student applies
✅ Message received: New message notification
✅ Application accepted: Student notified when accepted
✅ Mission completed: End-of-mission notification
```

Features:
```
✅ In-app notifications
✅ Mark as read
✅ Link to the relevant resource
✅ Full history
```

### 🛡️ Admin Panel

```
✅ Student account verification
✅ Reported mission moderation
✅ Reported profile moderation
✅ Mission category management
✅ Skills management
✅ Global statistics generation
✅ Django root admin access
```

---

## 🏗️ Architecture

### MVT Architecture (Model-View-Template) Django

```
StuLance/
│
├── Models (Data)
│   ├── User (Custom AbstractUser)
│   ├── StudentProfile & ClientProfile
│   ├── Mission, Application, Review
│   ├── Message (Messaging)
│   └── Notification
│
├── Views (Business logic)
│   ├── Accounts (Auth, profiles)
│   ├── Missions (CRUD, applications)
│   ├── Dashboard (Dashboards)
│   ├── Messaging (Conversations)
│   └── Notifications (Management)
│
└── Templates (Presentation)
    ├── Base layout
    ├── Server-side rendered HTML pages
    ├── Bootstrap 5 responsive
    └── Forms with validation
```

### Data Flow

```
Web Client (HTML/CSS/JS)
    ↓
Django URL Router
    ↓
Views (authentication + logic)
    ↓
Models (Django ORM)
    ↓
SQLite/MySQL Database
```

### Stateless Architecture (Sessions)

- No external JWT API
- Integrated Django sessions
- HttpOnly secure cookies
- CSRF tokens on all forms

---

## ⚙️ Tech Stack

| Component | Technology | Version | Reason |
|-----------|------------|---------|--------|
| **Backend** | Django | 4.x | Full-stack framework, powerful ORM, built-in security |
| **Frontend** | HTML5/CSS3/JS | - | Django templates (Jinja2), Bootstrap 5 responsive |
| **Database** | SQLite (dev) / MySQL | - | Lightweight in dev, performant in prod |
| **REST API** | Django REST Framework | - | JSON endpoints for future mobile |
| **Auth** | Django Auth System | - | Secure sessions, natively integrated |
| **File Storage** | Django FileField | - | Local in dev, S3 compatible in prod |
| **Versioning** | Git | - | GitHub for collaboration |
| **Deployment** | Gunicorn + Nginx | - | Linux VPS (Ubuntu 20.04+) |

### Python Dependencies (requirements.txt)
```
Django==4.2.x
djangorestframework
Pillow (Image processing)
mysql-connector-python (MySQL)
python-decouple (Environment variables)
```

---

## 📦 Installation

### Prerequisites

```bash
✅ Python 3.8+
✅ pip (package manager)
✅ Git
✅ MySQL 5.7+ (optional, SQLite by default)
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/ladroxd/StuLance.git
cd StuLance
```

### Step 2: Create the Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Apply Migrations

```bash
python manage.py migrate
```

### Step 4a: Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Follow the prompts
# Username: admin
# Email: admin@example.com
# Password: (secure)
```

### Step 5: Create Categories (Optional)

```bash
python manage.py shell
>>> from missions.models import Category
>>> Category.objects.create(name='Web Development', icon='code')
>>> Category.objects.create(name='Mobile App', icon='mobile')
>>> Category.objects.create(name='Design', icon='palette')
>>> Category.objects.create(name='Data Science', icon='chart')
>>> exit()
```

### Step 6: Start the Development Server

```bash
python manage.py runserver
```

✅ The application is accessible at: **http://127.0.0.1:8000/**

---

## 🔧 Configuration

`settings.py` is not committed to the repo because it contains secrets. Follow these steps to set it up locally.

### Step 1: Copy the example settings file

```bash
cp stulance/settings.example.py stulance/settings.py
```

On Windows:
```powershell
copy stulance\settings.example.py stulance\settings.py
```

### Step 2: Create the `.env` file

Create a `.env` file at the project root (next to `manage.py`):

**Quick start with SQLite (recommended for local dev):**

```env
SECRET_KEY=replace-this-with-a-long-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
USE_LOCAL_DB=1
```

**With MySQL (production / team setup):**

```env
SECRET_KEY=replace-this-with-a-long-random-string
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
USE_LOCAL_DB=0
DB_NAME=stulance_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

> **Generating a SECRET_KEY**: run this once and paste the output into `.env`:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### Step 3: Apply migrations and run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### MySQL Setup (if not using SQLite)

```bash
mysql -u root -p
> CREATE DATABASE stulance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> EXIT;
```

Then set `USE_LOCAL_DB=0` and fill in the `DB_*` variables in your `.env`.

---

## 🚀 Usage

### 1️⃣ Student Flow

```
1. Register → /accounts/register/student/
   - Email
   - Password
   - School & Field of study
   - Upload student card

2. Wait for verification (Admin validates the card)
   - Status: pending → verified

3. Create profile → /accounts/edit/
   - Bio, photo
   - Skills (tags)
   - GitHub/LinkedIn links
   - Portfolio (add projects)

4. Browse missions → /missions/
   - Filter by category, budget, duration
   - View details

5. Apply → /missions/<id>/apply/
   - Cover letter
   - Recruiter receives notification

6. Wait for acceptance
   - Notification if accepted
   - Access to messaging

7. Communicate → /messages/
   - Chat with the recruiter
   - Send deliverables

8. Closure & Rating
   - Mission marked complete by recruiter
   - Leave a review for the recruiter
   - Receive a rating
```

### 2️⃣ Recruiter Flow

```
1. Register → /accounts/register/client/
   - Email, password
   - Type (Company/Individual)
   - Company name

2. Create profile → /accounts/edit/
   - Bio, photo
   - Website
   - Description

3. Post a mission → /missions/create/
   - Detailed title
   - Full description
   - Budget in MAD
   - Duration (days)
   - Category
   - Required skills

4. Manage applications → /missions/<id>/applications/
   - View all applicants
   - Check their profiles & portfolios
   - Accept/Reject

5. Communicate → /messages/
   - Chat with selected student
   - Receive updates

6. Mark as completed
   - Verify deliverables
   - Close the mission

7. Leave a rating
   - 1-5 star evaluation
   - Comment
   - Contributes to the student's average rating
```

### 3️⃣ Administrator Flow

```
1. Access admin panel → /admin/
   - Username: admin
   - Password: (created during setup)

2. Verify students
   - StudentProfile → Pending approvals
   - Validate or reject cards
   - Change verification_status

3. Moderate content
   - Delete reported missions
   - Delete suspicious profiles
   - Manage users

4. Manage categories
   - CRUD mission categories
   - Add/edit icons

5. View statistics
   - Number of users
   - Published missions
   - Conversion rate
```

---

## 📁 Project Structure

```
StuLance/
│
├── 📱 accounts/                    # User management
│   ├── models.py                   # User, StudentProfile, ClientProfile, PortfolioProject
│   ├── views.py                    # Auth, profile, portfolio
│   ├── forms.py                    # Registration & profile forms
│   ├── urls.py                     # Routes /accounts/*
│   ├── admin.py                    # Django admin configuration
│   └── migrations/                 # Database migrations
│
├── 🎯 missions/                    # Mission & application management
│   ├── models.py                   # Mission, Application, Review, Category
│   ├── views.py                    # CRUD missions, applications, ratings
│   ├── forms.py                    # MissionForm, ApplicationForm, ReviewForm
│   ├── urls.py                     # Routes /missions/*
│   ├── admin.py                    # Admin configuration
│   └── migrations/
│
├── 💬 messaging/                   # In-app messaging
│   ├── models.py                   # Message (per mission)
│   ├── views.py                    # Display/send messages
│   ├── urls.py                     # Routes /messages/*
│   ├── admin.py
│   └── migrations/
│
├── 📊 dashboard/                   # Dashboards
│   ├── models.py                   # (No models — uses Mission, Application)
│   ├── views.py                    # dashboard() — differentiated student/recruiter
│   ├── urls.py                     # Routes /dashboard/*
│   └── migrations/
│
├── 🔔 notifications/               # Notification system
│   ├── models.py                   # Notification
│   ├── utils.py                    # create_notification()
│   ├── views.py                    # Display notifications
│   ├── urls.py                     # Routes /notifications/*
│   └── migrations/
│
├── ⚙️ stulance/                    # Django project configuration
│   ├── settings.py                 # Config, INSTALLED_APPS, Database
│   ├── urls.py                     # Main router
│   ├── views.py                    # home()
│   ├── wsgi.py                     # WSGI server
│   └── asgi.py                     # ASGI server
│
├── 🎨 templates/                   # HTML templates
│   ├── base.html                   # Base layout (navbar, footer)
│   ├── home.html                   # Home page
│   ├── accounts/
│   │   ├── register_student.html
│   │   ├── register_client.html
│   │   ├── login.html
│   │   ├── student_profile.html
│   │   ├── student_profile_detail.html
│   │   ├── client_profile_detail.html
│   │   ├── edit_profile.html
│   │   └── portfolio_form.html
│   ├── missions/
│   │   ├── list.html               # All missions (with filtering)
│   │   ├── detail.html             # Mission detail + applications
│   │   ├── form.html               # Create/Edit mission
│   │   ├── apply.html              # Application form
│   │   ├── applications.html       # Recruiter application management
│   │   ├── review_form.html        # Leave a rating
│   │   ├── complete_confirm.html   # Confirm mission completion
│   │   └── confirm_delete.html     # Confirm deletion
│   ├── dashboard/
│   │   ├── student.html            # Student dashboard
│   │   └── client.html             # Recruiter dashboard
│   ├── messaging/
│   │   └── conversation.html       # Message conversation per mission
│   └── notifications/
│       └── list.html               # Notifications list
│
├── 🎯 static/                      # Static files
│   ├── css/
│   │   └── style.css               # Custom styles
│   └── js/
│       └── main.js                 # JavaScript scripts
│
├── 🌍 locale/                      # Translations (i18n)
│   ├── fr/LC_MESSAGES/django.po    # French translations
│   └── ar/LC_MESSAGES/django.po    # Arabic translations
│
├── 🗄️ db.sqlite3                  # Database (dev only)
│
├── 📝 manage.py                    # Django management script
├── 📦 requirements.txt             # Python dependencies
├── .env.example                    # Configuration example
├── .gitignore                      # Files to ignore
├── .gitattributes                  # Line endings
└── README.md                       # This documentation
```

---

## 🗄️ Data Models

### User (Custom AbstractUser)

```python
class User(AbstractUser):
    ROLE_STUDENT = 'student'
    ROLE_CLIENT = 'client'
    ROLE_ADMIN = 'admin'

    role = CharField(choices=ROLE_CHOICES)  # User type
    phone = CharField(max_length=20)
    created_at = DateTimeField(auto_now_add=True)

    Methods:
    - is_student()
    - is_client()
```

### StudentProfile

```python
class StudentProfile(models.Model):
    user = OneToOneField(User)
    bio = TextField()
    photo = ImageField()
    skills = CharField(max_length=500)  # "Python, Django, React"
    github_url = URLField()
    linkedin_url = URLField()
    school = CharField()
    field_of_study = CharField()
    student_card = FileField()  # Upload for verification
    verification_status = CharField(
        choices=['pending', 'verified', 'rejected']
    )
    average_rating = FloatField(default=0.0)
    total_missions = PositiveIntegerField()

    Methods:
    - skills_list()  # Returns list of skills
```

### ClientProfile

```python
class ClientProfile(models.Model):
    user = OneToOneField(User)
    client_type = CharField(choices=['company', 'individual'])
    company_name = CharField()
    bio = TextField()
    photo = ImageField()
    website = URLField()
    average_rating = FloatField(default=0.0)
```

### PortfolioProject

```python
class PortfolioProject(models.Model):
    student = ForeignKey(StudentProfile)
    title = CharField(max_length=200)
    description = TextField()
    url = URLField()
    image = ImageField()
    created_at = DateTimeField(auto_now_add=True)
```

### Mission

```python
class Mission(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client = ForeignKey(User, related_name='missions')
    title = CharField(max_length=300)
    description = TextField()
    category = ForeignKey(Category)
    skills_required = CharField(max_length=500)  # "Python, Django"
    budget = DecimalField(max_digits=10, decimal_places=2)  # MAD
    deadline_days = PositiveIntegerField()  # Duration in days
    status = CharField(choices=STATUS_CHOICES, default='open')
    selected_student = ForeignKey(User, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    Methods:
    - skills_list()
```

### Application

```python
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    mission = ForeignKey(Mission, related_name='applications')
    student = ForeignKey(User, related_name='applications')
    cover_letter = TextField()
    status = CharField(choices=STATUS_CHOICES, default='pending')
    applied_at = DateTimeField(auto_now_add=True)

    Constraints:
    - unique_together = ('mission', 'student')  # One application per mission
```

### Review

```python
class Review(models.Model):
    mission = ForeignKey(Mission)
    reviewer = ForeignKey(User, related_name='reviews_given')
    reviewee = ForeignKey(User, related_name='reviews_received')
    rating = PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)

    Constraints:
    - unique_together = ('mission', 'reviewer')  # One review per reviewer/mission
```

### Message

```python
class Message(models.Model):
    mission = ForeignKey(Mission, related_name='messages')
    sender = ForeignKey(User, related_name='sent_messages')
    content = TextField()
    sent_at = DateTimeField(auto_now_add=True)
    is_read = BooleanField(default=False)

    Ordering: sent_at (oldest to newest)
```

### Notification

```python
class Notification(models.Model):
    TYPE_CHOICES = [
        ('application', 'New application'),
        ('message', 'New message'),
        ('mission_accepted', 'Mission accepted'),
        ('mission_completed', 'Mission completed'),
    ]

    user = ForeignKey(User, related_name='notifications')
    notif_type = CharField(choices=TYPE_CHOICES)
    title = CharField(max_length=200)
    message = TextField()
    link = CharField(max_length=300)  # Resource URL
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
```

### Category

```python
class Category(models.Model):
    name = CharField(max_length=100, unique=True)
    icon = CharField(max_length=50)  # Bootstrap icon name
```

### Full ER Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User (Django)                           │
│  • id • username • email • password_hash • role • phone         │
│  • is_active • is_staff • is_superuser • created_at            │
└────────────────┬──────────────────────────────────────────────┬─┘
                 │                                              │
      ┌──────────▼────────────┐                  ┌─────────────▼──────────┐
      │  StudentProfile       │                  │  ClientProfile         │
      │  (1-to-1)             │                  │  (1-to-1)              │
      ├───────────────────────┤                  ├────────────────────────┤
      │ • bio                 │                  │ • client_type          │
      │ • photo               │                  │ • company_name         │
      │ • skills              │                  │ • bio                  │
      │ • github_url          │                  │ • photo                │
      │ • linkedin_url        │                  │ • website              │
      │ • school              │                  │ • average_rating       │
      │ • field_of_study      │                  └────────────────────────┘
      │ • student_card        │
      │ • verification_status │       ┌──────────────────────────┐
      │ • average_rating      │       │  PortfolioProject        │
      │ • total_missions      │       │  (1-to-Many)             │
      └───────────┬───────────┘       ├──────────────────────────┤
                  │                   │ • title                  │
                  │                   │ • description            │
                  │                   │ • url                    │
                  │                   │ • image                  │
                  │                   │ • created_at             │
                  │                   └──────────────────────────┘
                  │
       ┌──────────▼────────────────────────────────────────┐
       │                   Mission                         │
       │  (Many-to-1 from User as client)                  │
       ├─────────────────────────────────────────────────┤
       │ • title • description • category • skills_req    │
       │ • budget • deadline_days • status • client       │
       │ • selected_student • created_at • updated_at     │
       └────────┬────────────────────────────────────────┘
                │
       ┌────────┴─────────────────────────────────────────┐
       │                                                  │
    ┌──▼────────────────────┐             ┌─────────────▼─────────┐
    │    Application         │             │       Review          │
    │    (Many-to-1)         │             │   (Many-to-1)         │
    ├────────────────────────┤             ├───────────────────────┤
    │ • mission              │             │ • mission             │
    │ • student              │             │ • reviewer            │
    │ • cover_letter         │             │ • reviewee            │
    │ • status               │             │ • rating (1-5)        │
    │ • applied_at           │             │ • comment             │
    │                        │             │ • created_at          │
    │ UC: (mission, student) │             │                       │
    │                        │             │ UC: (mission, reviewer)
    └────────────────────────┘             └───────────────────────┘

    ┌──────────────────────────┐           ┌──────────────────────┐
    │       Message            │           │    Notification      │
    │    (Many-to-1)           │           │    (Many-to-1)       │
    ├──────────────────────────┤           ├──────────────────────┤
    │ • mission                │           │ • user               │
    │ • sender                 │           │ • notif_type         │
    │ • content                │           │ • title              │
    │ • sent_at                │           │ • message            │
    │ • is_read                │           │ • link               │
    │                          │           │ • is_read            │
    │                          │           │ • created_at         │
    └──────────────────────────┘           └──────────────────────┘

    ┌──────────────────────┐
    │     Category         │
    │   (1-to-Many)        │
    ├──────────────────────┤
    │ • name               │
    │ • icon               │
    └──────────────────────┘
```

---

## 🔌 API Endpoints

### Authentication & Accounts

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Home page | - |
| GET/POST | `/accounts/register/student/` | Student registration | - |
| GET/POST | `/accounts/register/client/` | Recruiter registration | - |
| GET/POST | `/accounts/login/` | Sign in | - |
| POST | `/accounts/logout/` | Sign out | ✓ |
| GET | `/accounts/profile/` | View my profile | ✓ |
| GET/POST | `/accounts/edit/` | Edit profile | ✓ |
| GET/POST | `/accounts/portfolio/add/` | Add project | ✓ Student |
| GET | `/accounts/student/<id>/` | View student profile | - |
| GET | `/accounts/client/<id>/` | View recruiter profile | - |

### Missions

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/missions/` | List open missions | - |
| GET | `/missions/<id>/` | Mission details | - |
| GET/POST | `/missions/create/` | Create mission | ✓ Recruiter |
| GET/POST | `/missions/<id>/edit/` | Edit mission | ✓ Owner |
| POST | `/missions/<id>/delete/` | Delete mission | ✓ Owner |
| GET | `/missions/<id>/applications/` | View applications | ✓ Owner |

### Applications

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET/POST | `/missions/<id>/apply/` | Apply | ✓ Student |
| POST | `/applications/<id>/accept/` | Accept application | ✓ Owner |
| POST | `/applications/<id>/reject/` | Reject application | ✓ Owner |

### Mission Actions

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/missions/<id>/complete/` | Mark as completed | ✓ Recruiter |
| GET/POST | `/missions/<id>/review/` | Leave a rating | ✓ |

### Messaging

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/messages/<mission_id>/` | Mission conversation | ✓ |
| POST | `/messages/<mission_id>/send/` | Send message | ✓ |

### Notifications

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/notifications/` | List notifications | ✓ |
| POST | `/notifications/<id>/mark-read/` | Mark as read | ✓ |

### Dashboard

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/dashboard/` | Dashboard | ✓ |

### Admin

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET/POST | `/admin/` | Django admin panel | ✓ Superuser |

---

## 🔐 Security & Authentication

### Built-in Security Mechanisms

#### 1. **Django Authentication**
```python
✅ Native Django authentication system
✅ Hashed password storage (PBKDF2 by default)
✅ Secure sessions (session ID + cookie)
✅ HttpOnly cookies (no JavaScript access)
✅ Secure flag on HTTPS cookies
```

#### 2. **CSRF Protection (Cross-Site Request Forgery)**
```python
✅ Automatic CSRF middleware
✅ CSRF tokens on all forms
✅ SameSite cookies
```

#### 3. **Access Control (Authorization)**
```python
✅ @login_required on protected views
✅ user.is_student() / user.is_client() checks
✅ user == requester ownership verification
✅ Object-level permission checks
```

#### 4. **XSS Protection (Cross-Site Scripting)**
```python
✅ Django template auto-escape {{ variable }}
✅ No direct access to unvalidated HTML
✅ Django forms used (sanitization)
```

#### 5. **SQL Injection Protection**
```python
✅ Django ORM (no raw SQL)
✅ Parameterized queries
✅ Secure QuerySet API
```

#### 6. **File Uploads**
```python
✅ Storage outside web root (/media_uploads/)
✅ File type validation (FileField)
✅ Random name generation
✅ Files cannot be executed
```

#### 7. **Sensitive Data**
```python
✅ No hardcoded tokens
✅ No exposed public API keys
✅ Unique and secure SECRET_KEY
✅ DEBUG=False in production
```

### Student Status Verification

```python
# Manual process to prevent fraud
1. Student uploads student card
2. Administrator verifies manually
   - Image check
   - Validity verification
   - Update: STATUS_PENDING → STATUS_VERIFIED/REJECTED
3. Student notified of status
4. Access to certain features conditioned on verified=True
```

### Password Policy

```python
VALIDATORS:
✅ MinimumLengthValidator (8 characters)
✅ UserAttributeSimilarityValidator (no identifiers inside)
✅ CommonPasswordValidator (no common passwords)
✅ NumericPasswordValidator (not all digits)
```

---

## 🧪 Tests

### Run Tests

```bash
# All tests
python manage.py test

# Tests for a specific app
python manage.py test accounts
python manage.py test missions
python manage.py test messaging
python manage.py test notifications

# Tests for a specific class
python manage.py test accounts.tests.UserModelTests

# Tests with verbosity
python manage.py test --verbosity=2

# Tests with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Test Structure

```
accounts/tests.py          # Model and view tests
missions/tests.py          # Mission CRUD tests
messaging/tests.py         # Messaging tests
notifications/tests.py     # Notification tests
```

### Example Test

```python
from django.test import TestCase
from accounts.models import User, StudentProfile

class StudentProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        self.profile = StudentProfile.objects.create(
            user=self.user,
            school='EMSI',
            field_of_study='3IIR'
        )

    def test_student_creation(self):
        self.assertEqual(self.user.is_student(), True)
        self.assertEqual(self.profile.verification_status, 'pending')

    def test_skills_list(self):
        self.profile.skills = "Python, Django, React"
        skills = self.profile.skills_list()
        self.assertEqual(len(skills), 3)
```

---

## 🌐 Deployment

### Deploying on Linux VPS (Ubuntu 20.04+)

#### 1. Prepare the Server

```bash
# SSH into the server
ssh root@your_server_ip

# Update the system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv python3-dev
sudo apt install -y mysql-server nginx git
sudo apt install -y supervisor
```

#### 2. Clone the Project

```bash
cd /home
git clone https://github.com/ladroxd/StuLance.git
cd StuLance
```

#### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 4. Django Production Configuration

```bash
# Create .env file
nano .env

# Content:
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.mysql
DB_NAME=stulance_db
DB_USER=stulance_user
DB_PASSWORD=strong_password
DB_HOST=localhost
DB_PORT=3306
```

#### 5. Configure MySQL

```bash
sudo mysql
> CREATE DATABASE stulance_db CHARACTER SET utf8mb4;
> CREATE USER 'stulance_user'@'localhost' IDENTIFIED BY 'strong_password';
> GRANT ALL PRIVILEGES ON stulance_db.* TO 'stulance_user'@'localhost';
> FLUSH PRIVILEGES;
> EXIT;
```

#### 6. Apply Migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### 7. Configure Gunicorn

```bash
# Test Gunicorn
gunicorn --bind 0.0.0.0:8000 stulance.wsgi:application

# Create systemd file
sudo nano /etc/systemd/system/stulance.service
```

**Service file content**:
```ini
[Unit]
Description=StuLance Gunicorn Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/home/StuLance
Environment="PATH=/home/StuLance/venv/bin"
ExecStart=/home/StuLance/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/StuLance/stulance.sock \
    stulance.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Enable the service
sudo systemctl daemon-reload
sudo systemctl enable stulance
sudo systemctl start stulance
```

#### 8. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/stulance
```

**Nginx file content**:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/StuLance/staticfiles/;
    }

    location /media/ {
        alias /home/StuLance/media_uploads/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/StuLance/stulance.sock;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/stulance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 9. SSL with Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 📚 Documentation

### Documentation Files

- `README.md` - Project overview
- `INSTALLATION.md` - Detailed installation guide
- `API_DOCS.md` - API documentation (optional)
- `DEPLOYMENT.md` - Deployment guide (optional)
- Well-commented code with docstrings

### Useful Resources

- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Django Models](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/4.2/topics/http/views/)
- [Django ORM](https://docs.djangoproject.com/en/4.2/topics/db/queries/)
- [Django Security](https://docs.djangoproject.com/en/4.2/topics/security/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

### How to Contribute

1. **Fork** the repository
```bash
git clone https://github.com/yourusername/StuLance.git
```

2. **Create a branch** for your feature
```bash
git checkout -b feature/YourFeatureName
```

3. **Commit** your changes
```bash
git commit -m "Add your feature description"
```

4. **Push** to your fork
```bash
git push origin feature/YourFeatureName
```

5. **Open a Pull Request** with a detailed description

### Code Standards

```python
# Explicit names
user_profile ✓      # Instead of up
student_missions ✓  # Instead of sm

# Docstrings on complex functions
def get_active_missions(user):
    """
    Returns active missions where the user is selected.

    Args:
        user: The user to search missions for

    Returns:
        QuerySet: in_progress missions with the user selected
    """
    return Mission.objects.filter(
        selected_student=user,
        status='in_progress'
    )

# Follow PEP 8
# - 4 spaces indentation
# - Max 79 characters per line
# - Spaces around operators
```

### Issues & Bugs

If you find a bug or have a suggestion:

1. Open an [Issue](https://github.com/ladroxd/StuLance/issues) on GitHub
2. Describe the problem in detail
3. Provide steps to reproduce
4. Include screenshots if possible

---

## 📋 Future Roadmap

### Phase 2 (Short term)

- [ ] Integrated payment system (Stripe / CMI)
  - Secure transactions
  - Payment history
  - Automatic invoices

- [ ] Full REST API
  - JSON endpoints for mobile
  - Swagger/OpenAPI documentation
  - Rate limiting & throttling

- [ ] Recommendation system
  - AI-powered mission suggestions
  - AI-powered student suggestions
  - ML models

### Phase 3 (Medium term)

- [ ] Native mobile application
  - iOS with Swift
  - Android with Kotlin
  - Push notifications

- [ ] Automatic student card verification
  - OCR (Optical Character Recognition)
  - Facial recognition (optional)
  - Real-time validation

### Phase 4 (Long term)

- [ ] University integration
  - Moroccan university APIs
  - Data synchronisation
  - Official certification

- [ ] Accounting & tax management
  - Invoice generation
  - Tax calculation
  - Accounting export

- [ ] Certification system
  - Completion certificates
  - Skills badges
  - Skills verification

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

```
MIT License

Copyright (c) 2026 NAHAIRY Zakaria

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🤝 Support & Contact

- **GitHub Issues**: [StuLance Issues](https://github.com/ladroxd/StuLance/issues)
- **Email**: znahairy@gmail.com
- **Discord**: ladro. / **Telegram**: ladro_xd

---

## 📊 Project Statistics

```
📁 Directories: 10+
📄 Python files: 50+
📋 Lines of code: 2000+
🗄️ Models: 8
🔌 Endpoints: 30+
⚙️ Features: 25+
🧪 Tests: In progress
📝 Documentation: Complete
```

---

## 📅 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | March 2026 | Full initial release |
| 0.9.0 | February 2026 | Public beta |
| 0.5.0 | January 2026 | Development phase |

---

**Last updated**: May 2026
**Status**: 🟢 Active & Maintained
**Current Version**: 1.0.0

---

## 🚀 Get Started Now!

```bash
# 1. Clone the project
git clone https://github.com/ladroxd/StuLance.git

# 2. Install
cd StuLance
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 3. Configure settings
cp stulance/settings.example.py stulance/settings.py
# Create .env at project root — see Configuration section above

# 4. Setup database
python manage.py migrate
python manage.py createsuperuser

# 5. Run
python manage.py runserver

# 6. Access
# Web:   http://127.0.0.1:8000
# Admin: http://127.0.0.1:8000/admin
```

**Welcome to StuLance! 🎓💼**

---

### Questions? Check the [Full Documentation](https://github.com/ladroxd/StuLance/wiki) or open an [Issue](https://github.com/ladroxd/StuLance/issues)!

**Happy Coding! 💻✨**
