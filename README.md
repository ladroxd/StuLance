# 🚀 StuLance - Plateforme de Freelancing Académique

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/ladroxd/StuLance)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.x-darkgreen.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-brightblue.svg)](#)

**StuLance** est une plateforme web innovante permettant aux **étudiants marocains** de valoriser leurs compétences en tant que freelancers tout en offrant aux clients (entreprises, startups, particuliers) un moyen sécurisé et fiable de recruter des talents qualifiés.

> 💡 **Résolvant un problème réel** : Comment permettre aux étudiants d'accéder à des opportunités freelance adaptées à leur disponibilité académique, dans un environnement sécurisé et conforme au contexte marocain ?

---

## 📑 Table des Matières

1. [🎯 Aperçu du Projet](#-aperçu-du-projet)
2. [✨ Fonctionnalités](#-fonctionnalités)
3. [🏗️ Architecture](#️-architecture)
4. [⚙️ Stack Technologique](#️-stack-technologique)
5. [📦 Installation](#-installation)
6. [🔧 Configuration](#-configuration)
7. [🚀 Utilisation](#-utilisation)
8. [📁 Structure du Projet](#-structure-du-projet)
9. [🗄️ Modèles de Données](#️-modèles-de-données)
10. [🔌 API Endpoints](#-api-endpoints)
11. [🔐 Sécurité & Authentification](#-sécurité--authentification)
12. [🧪 Tests](#-tests)
13. [🌐 Déploiement](#-déploiement)
14. [📚 Documentation](#-documentation)

---

## 🎯 Aperçu du Projet

### Context & Problématique

Le freelancing connaît une croissance exponentielle au niveau mondial. Les étudiants en informatique, design, marketing et gestion possèdent des compétences réelles mais manquent de plateformes adaptées à leur contexte académique marocain.

**Problèmes identifiés** :
- ❌ Plateformes existantes (Upwork, Fiverr) sont génériques et en anglais
- ❌ Pas d'adaptation au calendrier académique et contraintes des étudiants
- ❌ Absence de vérification du statut étudiant
- ❌ Complexité pour les utilisateurs marocains

**La Solution** : **StuLance** - Une plateforme dédiée, sécurisée et adaptée au contexte académique marocain.

### Objectifs

**Généraux** :
- ✅ Créer une plateforme web permettant aux étudiants de proposer leurs services
- ✅ Permettre aux clients de publier des missions et recruter des talents
- ✅ Offrir un environnement sécurisé, transparent et académiquement adapté

**Spécifiques** :
- ✅ Système de profils avec portfolio et compétences
- ✅ Moteur de recherche et mise en relation client/étudiant
- ✅ Système de suivi des missions et notation mutuelle
- ✅ Vérification du statut étudiant via carte étudiante
- ✅ Back-office d'administration pour modération

---

## ✨ Fonctionnalités

### 👤 Gestion des Utilisateurs et Profils

#### Inscription & Authentification
```
✅ Inscription sécurisée pour étudiants et clients
✅ Authentification par email/mot de passe
✅ Session Django sécurisée (CSRF protection)
✅ Création automatique du profil lors de l'inscription
```

#### Profils Étudiants
```
✅ Upload de carte étudiante pour vérification
✅ Vérification manuelle par administrateur (pending/verified/rejected)
✅ Bio, photo de profil, compétences (tags)
✅ Liens GitHub et LinkedIn
✅ Informations académiques (école, filière)
✅ Portfolio avec projets réalisés
✅ Notation moyenne et statistiques de missions
```

#### Profils Clients
```
✅ Type client (Entreprise ou Particulier)
✅ Nom de l'entreprise/personne
✅ Bio, photo de profil
✅ Site web
✅ Notation moyenne
```

### 🎯 Gestion des Missions

#### Publication de Missions
```
✅ Titre, description détaillée
✅ Budget en MAD (Dirham marocain)
✅ Durée en jours
✅ Catégorie de mission
✅ Compétences requises
✅ Statut : Ouverte → En cours → Terminée → Notée
```

#### Recherche & Filtrage
```
✅ Recherche par mots-clés
✅ Filtrage par catégorie
✅ Filtrage par budget (min/max)
✅ Filtrage par durée
✅ Affichage des missions ouvertes uniquement
```

#### Cycles de Vie
```
Open (Ouverte)
  ↓
In Progress (Acceptée)
  ↓
Completed (Terminée)
  ↓
Reviewed (Notée)
```

### 📋 Système de Candidatures

```
✅ Postuler avec lettre de motivation
✅ Statut : Pending → Accepted → Rejected
✅ Un étudiant ne peut postuler qu'une fois par mission
✅ Client voir tous les candidats et leurs profils
✅ Acceptation crée une notification
✅ Rejet automatique des autres candidats
✅ Mise à jour du compteur de missions étudiantes
```

### 💬 Messagerie & Communication

```
✅ Messagerie contextualisée par mission
✅ Conversation entre étudiant et client
✅ Historique des messages
✅ Marquage comme lu/non lu
✅ Notifications de nouveaux messages
✅ Lien direct depuis chaque mission
```

### 📊 Tableaux de Bord

#### Dashboard Étudiant
```
✅ Candidatures en cours (pending)
✅ Missions acceptées (in_progress)
✅ Missions complétées (completed)
✅ Note moyenne reçue
✅ Total de missions réalisées
✅ Accès rapide au profil et portfolio
```

#### Dashboard Client
```
✅ Missions publiées (open, in_progress, completed)
✅ Candidatures reçues par mission
✅ Profils des candidats
✅ Boutons pour accepter/refuser
✅ Historique des missions passées
✅ Gestion du compte
```

### ⭐ Système de Notation & Avis

```
✅ Notation 1-5 étoiles + commentaire
✅ Après clôture de mission seulement
✅ Notation bilatérale (client → étudiant et inverse)
✅ Calcul automatique de la note moyenne
✅ Affichage des avis sur les profils
✅ Unique par paire (mission, reviewer)
```

### 🔔 Notifications

Types de notifications :
```
✅ Nouvelle candidature : Client notifié quand étudiant postule
✅ Message reçu : Notification de nouveau message
✅ Candidature acceptée : Étudiant notifié quand accepté
✅ Mission terminée : Notification de fin de mission
```

Features :
```
✅ In-app notifications
✅ Marquage comme lu
✅ Lien vers la ressource concernée
✅ Historique complet
```

### 🛡️ Panel d'Administration

```
✅ Vérification des comptes étudiants
✅ Modération des missions signalées
✅ Modération des profils signalés
✅ Gestion des catégories de missions
✅ Gestion des compétences
✅ Génération de statistiques globales
✅ Accès root Django admin
```

---

## 🏗️ Architecture

### Architecture MVT (Model-View-Template) Django

```
StuLance/
│
├── Models (Données)
│   ├── User (Custom AbstractUser)
│   ├── StudentProfile & ClientProfile
│   ├── Mission, Application, Review
│   ├── Message (Messaging)
│   └── Notification
│
├── Views (Logique métier)
│   ├── Accounts (Auth, profils)
│   ├── Missions (CRUD, candidatures)
│   ├── Dashboard (Tableaux de bord)
│   ├── Messaging (Conversations)
│   └── Notifications (Gestion)
│
└── Templates (Présentation)
    ├── Base layout
    ├── Pages HTML rendues côté serveur
    ├── Bootstrap 5 responsive
    └── Forms avec validation
```

### Flux de Données

```
Client Web (HTML/CSS/JS)
    ↓
Django URL Router
    ↓
Views (authentification + logique)
    ↓
Models (ORM Django)
    ↓
SQLite/MySQL Database
```

### Stateless Architecture (Sessions)

- Pas d'API JWT externe
- Sessions Django intégrées
- Cookies HttpOnly sécurisés
- CSRF tokens sur tous les formulaires

---

## ⚙️ Stack Technologique

| Composant | Technologie | Version | Raison |
|-----------|-------------|---------|--------|
| **Backend** | Django | 4.x | Framework full-stack, ORM puissant, sécurité intégrée |
| **Frontend** | HTML5/CSS3/JS | - | Templates Django (Jinja2), Bootstrap 5 responsive |
| **Database** | SQLite (dev) / MySQL | - | Léger en dev, performant en prod |
| **API REST** | Django REST Framework | - | Endpoints JSON pour messagerie future |
| **Auth** | Django Auth System | - | Sessions sécurisées, intégré nativement |
| **File Storage** | Django FileField | - | Local en dev, S3 compatible en prod |
| **Versioning** | Git | - | GitHub pour collaboration |
| **Deployment** | Gunicorn + Nginx | - | VPS Linux (Ubuntu 20.04+) |

### Dépendances Python (requirements.txt)
```
Django==4.2.x
djangorestframework
Pillow (Image processing)
mysql-connector-python (MySQL)
python-decouple (Environment variables)
```

---

## 📦 Installation

### Prérequis

```bash
✅ Python 3.8+
✅ pip (gestionnaire de paquets)
✅ Git
✅ MySQL 5.7+ (optionnel, SQLite par défaut)
```

### Étape 1 : Cloner le Repository

```bash
git clone https://github.com/ladroxd/StuLance.git
cd StuLance
```

### Étape 2 : Créer l'Environnement Virtuel

```bash
# Sur Windows
python -m venv venv
venv\Scripts\activate

# Sur macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer les Dépendances

```bash
pip install -r requirements.txt
```

### Étape 4 : Appliquer les Migrations

```bash
python manage.py migrate
```

### Étape 4a : Créer le Superutilisateur (Admin)

```bash
python manage.py createsuperuser
# Suivre les prompts
# Username: admin
# Email: admin@example.com
# Password: (sécurisé)
```

### Étape 5 : Créer les Catégories (Optional)

```bash
python manage.py shell
>>> from missions.models import Category
>>> Category.objects.create(name='Web Development', icon='code')
>>> Category.objects.create(name='Mobile App', icon='mobile')
>>> Category.objects.create(name='Design', icon='palette')
>>> Category.objects.create(name='Data Science', icon='chart')
>>> exit()
```

### Étape 6 : Lancer le Serveur de Développement

```bash
python manage.py runserver
```

✅ L'application est accessible à : **http://127.0.0.1:8000/**

---

## 🔧 Configuration

### Variables d'Environnement (.env)

Créer un fichier `.env` à la racine du projet :

```env
# Django Configuration
SECRET_KEY=your-long-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite - défaut)
DB_ENGINE=django.db.backends.sqlite3

# Database (MySQL - production)
# DB_ENGINE=django.db.backends.mysql
# DB_NAME=stulance_db
# DB_USER=root
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=3306

# Email (optionnel)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# AWS S3 (optionnel - production)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

### Configuration MySQL (Production)

```bash
# 1. Créer la base de données
mysql -u root -p
> CREATE DATABASE stulance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> EXIT;

# 2. Mettre à jour .env avec les infos MySQL

# 3. Appliquer les migrations
python manage.py migrate

# 4. Créer le superuser
python manage.py createsuperuser
```

### Fichier .gitignore (déjà inclus)

```
*.pyc
__pycache__/
*.sqlite3
.env
venv/
.vscode/
.idea/
*.log
.DS_Store
/staticfiles/
/media_uploads/
```

---

## 🚀 Utilisation

### 1️⃣ Flux Étudiant

```
1. S'inscrire → /accounts/register/student/
   - Email
   - Mot de passe
   - École & Filière
   - Upload carte étudiante
   
2. Attendre vérification (Admin valide la carte)
   - Statut: pending → verified
   
3. Créer profil → /accounts/edit/
   - Bio, photo
   - Compétences (tags)
   - Liens GitHub/LinkedIn
   - Portfolio (ajouter projets)
   
4. Chercher missions → /missions/
   - Filtrer par catégorie, budget, durée
   - Consulter détails
   
5. Postuler → /missions/<id>/apply/
   - Lettre de motivation
   - Client reçoit notification
   
6. Attendre acceptation
   - Notification si accepté
   - Accès à la messagerie
   
7. Communiquer → /messages/
   - Discuter avec le client
   - Envoyer livrables
   
8. Clôture & Notation
   - Mission marquée terminée par client
   - Laisser avis sur client
   - Reçevoir notation
```

### 2️⃣ Flux Client

```
1. S'inscrire → /accounts/register/client/
   - Email, mot de passe
   - Type (Entreprise/Particulier)
   - Nom entreprise
   
2. Créer profil → /accounts/edit/
   - Bio, photo
   - Site web
   - Description
   
3. Publier mission → /missions/create/
   - Titre détaillé
   - Description complète
   - Budget MAD
   - Durée (jours)
   - Catégorie
   - Compétences requises
   
4. Gérer candidatures → /missions/<id>/applications/
   - Voir tous les candidats
   - Consulter leurs profils
   - Portfolio & portfolio
   - Accepter/Refuser
   
5. Communiquer → /messages/
   - Discuter avec étudiant sélectionné
   - Recevoir mises à jour
   
6. Marquer comme terminée
   - Vérifier livrables
   - Clôturer mission
   
7. Laisser notation
   - Évaluation 1-5 étoiles
   - Commentaire
   - Vote pour la note moyenne de l'étudiant
```

### 3️⃣ Flux Administrateur

```
1. Accéder au panel admin → /admin/
   - Username: admin
   - Password: (créé lors du setup)
   
2. Vérifier les étudiants
   - StudentProfile → Pending approvals
   - Valider ou rejeter les cartes
   - Changer verification_status
   
3. Modérer le contenu
   - Supprimer missions signalées
   - Supprimer profils suspects
   - Gérer utilisateurs
   
4. Gérer les catégories
   - CRUD catégories de missions
   - Ajouter/éditer les icons
   
5. Consulter statistiques
   - Nombre d'utilisateurs
   - Missions publiées
   - Taux de conversion
```

---

## 📁 Structure du Projet

```
StuLance/
│
├── 📱 accounts/                    # Gestion des utilisateurs
│   ├── models.py                   # User, StudentProfile, ClientProfile, PortfolioProject
│   ├── views.py                    # Auth, profil, portfolio
│   ├── forms.py                    # Formulaires inscription & profil
│   ├── urls.py                     # Routes /accounts/*
│   ├── admin.py                    # Configuration admin Django
│   └── migrations/                 # Migrations base de données
│
├── 🎯 missions/                    # Gestion des missions & candidatures
│   ├── models.py                   # Mission, Application, Review, Category
│   ├── views.py                    # CRUD missions, candidatures, notation
│   ├── forms.py                    # MissionForm, ApplicationForm, ReviewForm
│   ├── urls.py                     # Routes /missions/*
│   ├── admin.py                    # Configuration admin
│   └── migrations/
│
├── 💬 messaging/                   # Messagerie in-app
│   ├── models.py                   # Message (par mission)
│   ├── views.py                    # Afficher/envoyer messages
│   ├── urls.py                     # Routes /messages/*
│   ├── admin.py
│   └── migrations/
│
├── 📊 dashboard/                   # Tableaux de bord
│   ├── models.py                   # (Pas de modèles - utilise Mission, Application)
│   ├── views.py                    # dashboard() - différencié student/client
│   ├── urls.py                     # Routes /dashboard/*
│   └── migrations/
│
├── 🔔 notifications/               # Système de notifications
│   ├── models.py                   # Notification
│   ├── utils.py                    # create_notification()
│   ├── views.py                    # Afficher notifications
│   ├── urls.py                     # Routes /notifications/*
│   └── migrations/
│
├── ⚙️ stulance/                    # Configuration Django (projet)
│   ├── settings.py                 # Configurations, INSTALLED_APPS, Database
│   ├── urls.py                     # Router principal (path('accounts/', ...) etc)
│   ├── views.py                    # home()
│   ├── wsgi.py                     # WSGI server
│   └── asgi.py                     # ASGI server
│
├── 🎨 templates/                   # Templates HTML
│   ├── base.html                   # Layout de base (navbar, footer)
│   ├── home.html                   # Page d'accueil
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
│   │   ├── list.html               # Affiche toutes les missions (filtrage)
│   │   ├── detail.html             # Détail mission + candidatures
│   │   ├── form.html               # Create/Edit mission
│   │   ├── apply.html              # Form de candidature
│   │   ├── applications.html       # Admin candidatures par client
│   │   ├── review_form.html        # Laisser notation
│   │   ├── complete_confirm.html   # Confirmer fin de mission
│   │   └── confirm_delete.html     # Confirmer suppression
│   ├── dashboard/
│   │   ├── student.html            # Dashboard étudiant
│   │   └── client.html             # Dashboard client
│   ├── messaging/
│   │   └── conversation.html       # Conversation messages/mission
│   └── notifications/
│       └── list.html               # Liste notifications
│
├── 🎯 static/                      # Fichiers statiques
│   ├── css/
│   │   └── style.css               # Styles personnalisés
│   └── js/
│       └── main.js                 # Scripts JavaScript
│
├── 📁 media_uploads/               # Uploads utilisateurs
│   ├── profiles/
│   │   ├── students/               # Photos étudiants
│   │   └── clients/                # Photos clients
│   ├── student_cards/              # Cartes étudiantes uploadées
│   └── portfolio/                  # Images portfolio
│
├── 🗄️ db.sqlite3                  # Base de données (dev uniquement)
│
├── 📝 manage.py                    # Script management Django
├── 📦 requirements.txt             # Dépendances Python
├── .env.example                    # Exemple de configuration
├── .gitignore                      # Fichiers à ignorer
├── .gitattributes                  # Ligne endings
└── README.md                       # Cette documentation
```

---

## 🗄️ Modèles de Données

### User (Custom AbstractUser)

```python
class User(AbstractUser):
    ROLE_STUDENT = 'student'
    ROLE_CLIENT = 'client'
    ROLE_ADMIN = 'admin'
    
    role = CharField(choices=ROLE_CHOICES)  # Type d'utilisateur
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
    student_card = FileField()  # Upload pour vérification
    verification_status = CharField(
        choices=['pending', 'verified', 'rejected']
    )
    average_rating = FloatField(default=0.0)
    total_missions = PositiveIntegerField()
    
    Methods:
    - skills_list()  # Retourne liste de compétences
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
        ('open', 'Ouverte'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    ]
    
    client = ForeignKey(User, related_name='missions')
    title = CharField(max_length=300)
    description = TextField()
    category = ForeignKey(Category)
    skills_required = CharField(max_length=500)  # "Python, Django"
    budget = DecimalField(max_digits=10, decimal_places=2)  # MAD
    deadline_days = PositiveIntegerField()  # Durée en jours
    status = CharField(choices=STATUS_CHOICES, default='open')
    selected_student = ForeignKey(User, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    Methods:
    - skills_list()
```

### Application (Candidature)

```python
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Refusée'),
    ]
    
    mission = ForeignKey(Mission, related_name='applications')
    student = ForeignKey(User, related_name='applications')
    cover_letter = TextField()  # Lettre de motivation
    status = CharField(choices=STATUS_CHOICES, default='pending')
    applied_at = DateTimeField(auto_now_add=True)
    
    Constraints:
    - unique_together = ('mission', 'student')  # Une candidature par mission
```

### Review (Notation & Avis)

```python
class Review(models.Model):
    mission = ForeignKey(Mission)
    reviewer = ForeignKey(User, related_name='reviews_given')
    reviewee = ForeignKey(User, related_name='reviews_received')
    rating = PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    
    Constraints:
    - unique_together = ('mission', 'reviewer')  # Un avis par reviewer/mission
```

### Message

```python
class Message(models.Model):
    mission = ForeignKey(Mission, related_name='messages')
    sender = ForeignKey(User, related_name='sent_messages')
    content = TextField()
    sent_at = DateTimeField(auto_now_add=True)
    is_read = BooleanField(default=False)
    
    Ordering: sent_at (du plus ancien au plus récent)
```

### Notification

```python
class Notification(models.Model):
    TYPE_CHOICES = [
        ('application', 'Nouvelle candidature'),
        ('message', 'Nouveau message'),
        ('mission_accepted', 'Mission acceptée'),
        ('mission_completed', 'Mission terminée'),
    ]
    
    user = ForeignKey(User, related_name='notifications')
    notif_type = CharField(choices=TYPE_CHOICES)
    title = CharField(max_length=200)
    message = TextField()
    link = CharField(max_length=300)  # URL de la ressource
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
```

### Category

```python
class Category(models.Model):
    name = CharField(max_length=100, unique=True)
    icon = CharField(max_length=50)  # Font Awesome ou emoji
```

### Diagramme ER Complet

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
      │ • field_of_study      │                  │ • average_rating       │
      │ • student_card        │                  └────────────────────────┘
      │ • verification_status │
      │ • average_rating      │       ┌──────────────────────────┐
      │ • total_missions      │       │  PortfolioProject        │
      └───────────┬───────────┘       │  (1-to-Many)             │
                  │                   ├──────────────────────────┤
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

### Authentification & Comptes

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/` | Page d'accueil | - |
| GET/POST | `/accounts/register/student/` | Inscription étudiant | - |
| GET/POST | `/accounts/register/client/` | Inscription client | - |
| GET/POST | `/accounts/login/` | Connexion | - |
| POST | `/accounts/logout/` | Déconnexion | ✓ |
| GET | `/accounts/profile/` | Voir mon profil | ✓ |
| GET/POST | `/accounts/edit/` | Éditer profil | ✓ |
| GET/POST | `/accounts/portfolio/add/` | Ajouter projet | ✓ Étudiant |
| GET | `/accounts/student/<id>/` | Voir profil étudiant | - |
| GET | `/accounts/client/<id>/` | Voir profil client | - |

### Missions

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/missions/` | Lister missions ouvertes | - |
| GET | `/missions/<id>/` | Détails mission | - |
| GET/POST | `/missions/create/` | Créer mission | ✓ Client |
| GET/POST | `/missions/<id>/edit/` | Éditer mission | ✓ Client owner |
| POST | `/missions/<id>/delete/` | Supprimer mission | ✓ Client owner |
| GET | `/missions/<id>/applications/` | Voir candidatures | ✓ Client owner |

### Candidatures

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET/POST | `/missions/<id>/apply/` | Postuler | ✓ Étudiant |
| POST | `/applications/<id>/accept/` | Accepter candidature | ✓ Client owner |
| POST | `/applications/<id>/reject/` | Refuser candidature | ✓ Client owner |

### Missions (Actions)

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/missions/<id>/complete/` | Marquer comme terminée | ✓ Client |
| GET/POST | `/missions/<id>/review/` | Laisser notation | ✓ |

### Messagerie

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/messages/` | Lister conversations | ✓ |
| GET | `/messages/<mission_id>/` | Conversation mission | ✓ |
| POST | `/messages/<mission_id>/send/` | Envoyer message | ✓ |

### Notifications

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/notifications/` | Lister notifications | ✓ |
| POST | `/notifications/<id>/mark-read/` | Marquer comme lue | ✓ |

### Dashboard

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/dashboard/` | Tableau de bord | ✓ |

### Admin

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET/POST | `/admin/` | Django admin panel | ✓ Superuser |

---

## 🔐 Sécurité & Authentification

### Mécanismes de Sécurité Intégrés

#### 1. **Authentification Django**
```python
✅ Système d'authentification natif Django
✅ Stockage des mots de passe hashé (PBKDF2 par défaut)
✅ Sessions sécurisées (session ID + cookie)
✅ Cookies HttpOnly (pas d'accès JavaScript)
✅ Secure flag sur cookies HTTPS
```

#### 2. **Protection CSRF (Cross-Site Request Forgery)**
```python
✅ CSRF middleware automatique
✅ Tokens CSRF sur tous les formulaires
✅ SameSite cookies
```

#### 3. **Contrôle d'Accès (Authorization)**
```python
✅ @login_required sur les vues protégées
✅ Vérification user.is_student() / user.is_client()
✅ Vérification user == requester (ownership)
✅ Vérification des permissions sur les objets
```

#### 4. **Protection XSS (Cross-Site Scripting)**
```python
✅ Auto-escape des templates Django {{ variable }}
✅ Pas d'accès direct à HTML non validé
✅ Utilisation de formulaires Django (sanitization)
```

#### 5. **Protection SQL Injection**
```python
✅ ORM Django (pas de raw SQL)
✅ Parameterized queries
✅ QuerySet API sécurisée
```

#### 6. **Upload de Fichiers**
```python
✅ Stockage en dehors de la racine web (/media_uploads/)
✅ Validation du type de fichier (FileField)
✅ Génération de noms aléatoires
✅ Impossible d'exécuter les fichiers
```

#### 7. **Données Sensibles**
```python
✅ Pas de stockage de tokens en dur
✅ Pas de clés API publiques exposées
✅ SECRET_KEY unique et sécurisé
✅ DEBUG=False en production
```

### Vérification du Statut Étudiant

```python
# Processus manuel pour éviter les fraudes
1. Étudiant upload carte étudiante
2. Administrateur vérifie manuellement
   - Vérification de l'image
   - Vérification de la validité
   - Mise à jour: STATUS_PENDING → STATUS_VERIFIED/REJECTED
3. Étudiant notifié du statut
4. Accès aux certaines fonctionnalités conditionné à verified=True
```

### Politique de Mots de Passe

```python
VALIDATORS:
✅ MinimumLengthValidator (8 caractères)
✅ UserAttributeSimilarityValidator (pas d'identifiants dedans)
✅ CommonPasswordValidator (pas de mots de passe courants)
✅ NumericPasswordValidator (pas que des chiffres)
```

---

## 🧪 Tests

### Lancer les Tests

```bash
# Tous les tests
python manage.py test

# Tests d'une application spécifique
python manage.py test accounts
python manage.py test missions
python manage.py test messaging
python manage.py test notifications

# Tests d'une classe spécifique
python manage.py test accounts.tests.UserModelTests

# Tests avec verbosité
python manage.py test --verbosity=2

# Tests avec coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Générer rapport HTML
```

### Structure des Tests

```
accounts/tests.py          # Tests des modèles et vues
missions/tests.py          # Tests CRUD missions
messaging/tests.py         # Tests messagerie
notifications/tests.py     # Tests notifications
```

### Exemple de Test

```python
from django.test import TestCase
from accounts.models import User, StudentProfile

class StudentProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='etudiant',
            email='etudiant@example.com',
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

## 🌐 Déploiement

### Déploiement sur VPS Linux (Ubuntu 20.04+)

#### 1. Préparer le Serveur

```bash
# SSH dans le serveur
ssh root@your_server_ip

# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer les dépendances
sudo apt install -y python3-pip python3-venv python3-dev
sudo apt install -y mysql-server nginx git
sudo apt install -y supervisor
```

#### 2. Cloner le Projet

```bash
cd /home
git clone https://github.com/ladroxd/StuLance.git
cd StuLance
```

#### 3. Créer l'Environnement Virtuel

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 4. Configuration Django Production

```bash
# Créer fichier .env
nano .env

# Contenu:
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

#### 5. Configurer MySQL

```bash
sudo mysql
> CREATE DATABASE stulance_db CHARACTER SET utf8mb4;
> CREATE USER 'stulance_user'@'localhost' IDENTIFIED BY 'strong_password';
> GRANT ALL PRIVILEGES ON stulance_db.* TO 'stulance_user'@'localhost';
> FLUSH PRIVILEGES;
> EXIT;
```

#### 6. Appliquer les Migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### 7. Configurer Gunicorn

```bash
# Tester Gunicorn
gunicorn --bind 0.0.0.0:8000 stulance.wsgi:application

# Créer fichier systemd
sudo nano /etc/systemd/system/stulance.service
```

**Contenu du service** :
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
# Activer le service
sudo systemctl daemon-reload
sudo systemctl enable stulance
sudo systemctl start stulance
```

#### 8. Configurer Nginx

```bash
sudo nano /etc/nginx/sites-available/stulance
```

**Contenu du fichier Nginx** :
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
# Activer le site
sudo ln -s /etc/nginx/sites-available/stulance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 9. SSL avec Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 📚 Documentation

### Fichiers de Documentation

- `README.md` - Vue d'ensemble du projet
- `INSTALLATION.md` - Guide d'installation détaillé
- `API_DOCS.md` - Documentation API (optionnel)
- `DEPLOYMENT.md` - Guide de déploiement (optionnel)
- Code bien commenté avec docstrings

### Ressources Utiles

- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Django Models](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/4.2/topics/http/views/)
- [Django ORM](https://docs.djangoproject.com/en/4.2/topics/db/queries/)
- [Django Security](https://docs.djangoproject.com/en/4.2/topics/security/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)




### Comment Contribuer

1. **Fork** le repository
```bash
git clone https://github.com/yourusername/StuLance.git
```

2. **Créer une branche** pour votre feature
```bash
git checkout -b feature/YourFeatureName
```

3. **Commit** vos changements
```bash
git commit -m "Add your feature description"
```

4. **Push** vers votre fork
```bash
git push origin feature/YourFeatureName
```

5. **Ouvrir une Pull Request** avec une description détaillée

### Standards de Code

```python
# Noms explicites
user_profile ✓    # Au lieu de up
student_missions ✓ # Au lieu de sm

# Docstrings sur les fonctions complexes
def get_active_missions(user):
    """
    Retourne les missions actives où l'utilisateur est sélectionné.
    
    Args:
        user: L'utilisateur pour lequel chercher les missions
    
    Returns:
        QuerySet: Missions in_progress avec l'utilisateur sélectionné
    """
    return Mission.objects.filter(
        selected_student=user,
        status='in_progress'
    )

# Commentaires pour la logique complexe
# Rejeter automatiquement les autres candidatures
Application.objects.filter(mission=mission).exclude(pk=app_id).update(
    status='rejected'
)

# Suivre PEP 8
# - 4 espaces d'indentation
# - Lignes max 79 caractères
# - Espaces autour des opérateurs
```

### Issues & Bugs

Si vous trouvez un bug ou avez une suggestion :

1. Ouvrir une [Issue](https://github.com/ladroxd/StuLance/issues) sur GitHub
2. Décrire le problème en détail
3. Fournir les étapes pour reproduire
4. Inclure des screenshots si possible

---

## 📋 Roadmap Futures

### Phase 2 (Court terme)

- [ ] Système de paiement intégré (Stripe / CMI)
  - Transactions sécurisées
  - Historique des paiements
  - Factures automatiques

- [ ] API REST complète
  - Endpoints JSON pour mobile
  - Documentation Swagger/OpenAPI
  - Rate limiting & throttling

- [ ] Système de recommandation
  - Suggestions de missions par IA
  - Suggestions d'étudiants par IA
  - ML models

### Phase 3 (Moyen terme)

- [ ] Application mobile native
  - iOS avec Swift
  - Android avec Kotlin
  - Push notifications

- [ ] Vérification automatique de cartes étudiantes
  - OCR (Optical Character Recognition)
  - Reconnaissance faciale (optionnel)
  - Validation en temps réel

- [ ] Support multi-langue
  - Arabe (العربية)
  - Anglais (English)
  - Français (existant)

### Phase 4 (Long terme)

- [ ] Intégration avec les universités
  - API des universités marocaines
  - Synchronisation des données
  - Certification officielle

- [ ] Gestion comptable & fiscale
  - Génération de factures
  - Calcul de taxes
  - Export comptable

- [ ] Système de certification
  - Certificats de complétion
  - Badges de compétences
  - Vérification des compétences

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir [LICENSE](LICENSE) pour les détails.

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

- **Issues GitHub** : [StuLance Issues](https://github.com/ladroxd/StuLance/issues)
- **Email** : znahairy@gmail.com 
- **Discord/Slack** : Discord : ladro.   / Telegram :  ladro_xd

---

## 📊 Statistiques du Projet

```
📁 Dossiers : 10+
📄 Fichiers Python : 50+
📋 Lignes de Code : 2000+
🗄️ Modèles : 8
🔌 Endpoints : 30+
⚙️ Fonctionnalités : 25+
🧪 Tests : En cours
📝 Documentation : Complète
```

---




## 📅 Historique des Versions

| Version | Date | Changements |
|---------|------|-----------|
| 1.0.0 | Mars 2026 | Version initiale complète |
| 0.9.0 | Février 2026 | Bêta publique |
| 0.5.0 | Janvier 2026 | Phase de développement |

---

**Dernière mise à jour** : Mai 2026  
**Statut** : 🟢 Actif & Maintenu  
**Version Actuelle** : 1.0.0

---

## 🚀 Commencez Maintenant !

```bash
# 1. Cloner le projet
git clone https://github.com/ladroxd/StuLance.git

# 2. Installer
cd StuLance
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt

# 3. Configurer
python manage.py migrate
python manage.py createsuperuser

# 4. Lancer
python manage.py runserver

# 5. Accéder
# Web : http://127.0.0.1:8000
# Admin : http://127.0.0.1:8000/admin
```

**Bienvenue sur StuLance ! 🎓💼**

---

### Questions ? Consultez la [Documentation Complète](https://github.com/ladroxd/StuLance/wiki) ou ouvrez une [Issue](https://github.com/ladroxd/StuLance/issues) ! 

**Happy Coding! 💻✨**
