import random
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from accounts.models import User, StudentProfile, ClientProfile
from missions.models import Mission, Category
from gigs.models import Gig

STUDENTS = [
    ("Yassine Alami", "yassine.alami", "Casablanca", "EMSI", "Génie Informatique", "React, Django, Python, PostgreSQL", 150),
    ("Imane Benali", "imane.benali", "Rabat", "ENSIAS", "Data Science", "Python, Machine Learning, TensorFlow, Pandas", 180),
    ("Hamza Ouali", "hamza.ouali", "Casablanca", "ENSA", "Développement Mobile", "Flutter, Dart, Firebase, REST APIs", 120),
    ("Sara El Fassi", "sara.elfassi", "Marrakech", "EMSI", "Design UI/UX", "Figma, Adobe XD, Illustrator, CSS", 130),
    ("Mehdi Tazi", "mehdi.tazi", "Casablanca", "EMSI", "DevOps & Cloud", "Docker, Kubernetes, AWS, Linux", 200),
    ("Nour Cherkaoui", "nour.cherkaoui", "Fès", "UIR", "Marketing Digital", "SEO, Google Ads, Social Media, Copywriting", 100),
    ("Anas Berrada", "anas.berrada", "Casablanca", "ENSEM", "Réseaux & Systèmes", "Cisco, Linux, Python, Wireshark", 140),
    ("Leila Idrissi", "leila.idrissi", "Rabat", "UM5", "Rédaction & Contenu", "Rédaction FR/AR, SEO, WordPress, Canva", 90),
]

RECRUITERS = [
    ("TechCo Maroc", "techco", "Rachid Amrani", "Casablanca", "Startup tech spécialisée en SaaS B2B pour le marché africain."),
    ("DigitAgency", "digitagency", "Karim Bensouda", "Casablanca", "Agence digitale full-service : web, mobile, marketing."),
    ("DataVision", "datavision", "Fatima Zahrae Alj", "Rabat", "Cabinet de conseil en data analytics et BI."),
    ("PixelStudio", "pixelstudio", "Omar Lamrani", "Marrakech", "Studio de création graphique et UX/UI design."),
    ("CloudBase", "cloudbase", "Sanae Belhaj", "Casablanca", "Infrastructure cloud et cybersécurité pour PMEs marocaines."),
]

MISSIONS = [
    ("Développer une landing page React", "Developpement Web",
     "Nous cherchons un étudiant pour créer une landing page moderne avec React et Tailwind CSS. La page doit être responsive, rapide et optimisée SEO. Livraison en 7 jours.",
     1200, 7),
    ("Créer un dashboard analytics avec Python", "Data & IA",
     "Développer un dashboard interactif avec Plotly/Dash ou Streamlit pour visualiser des KPIs business. Données fournies en CSV.",
     1800, 14),
    ("Concevoir l'identité visuelle d'une startup", "Design & UI/UX",
     "Design du logo, charte graphique et supports de communication pour une startup fintech. Livrables : fichiers source Figma + exports.",
     2500, 10),
    ("Développer une app mobile Flutter", "Mobile",
     "Application de suivi de commandes pour un e-commerce local. iOS + Android. Backend REST déjà disponible.",
     3500, 21),
    ("Rédiger 10 articles SEO en français", "Redaction",
     "Articles de blog de 1000 mots chacun sur des sujets tech et startup au Maroc. Mots-clés fournis. Ton professionnel mais accessible.",
     900, 14),
    ("Audit et optimisation SEO du site web", "Marketing Digital",
     "Audit complet du site + rapport + mise en place des corrections on-page. Outils : Semrush ou Ahrefs. Livraison d'un rapport détaillé.",
     1500, 7),
    ("Configurer un serveur Linux + Nginx + SSL", "Reseaux & Systemes",
     "Mise en place d'un VPS Ubuntu avec Nginx, SSL Let's Encrypt, et déploiement d'une app Django. Documentation requise.",
     800, 5),
    ("Montage et post-production d'une vidéo corporate", "Video & Multimedia",
     "Montage d'une vidéo de présentation de 3 minutes pour une entreprise. Rushes fournis. Motion graphics simples attendus.",
     1100, 7),
    ("Créer un modèle de classification ML", "Data & IA",
     "Entraîner un modèle de classification pour détecter des fraudes dans des transactions bancaires. Dataset fourni. Rapport + code propre.",
     2200, 14),
    ("Développer une API REST Django", "Developpement Web",
     "API pour une app de gestion de stocks : CRUD produits, authentification JWT, documentation Swagger. Tests unitaires inclus.",
     1600, 10),
    ("Design UI/UX d'une app mobile", "Design & UI/UX",
     "Wireframes + maquettes haute fidélité pour une app de livraison de repas au Maroc. User flows, composants Figma, prototype cliquable.",
     1900, 12),
    ("Campagne Google Ads + Meta Ads", "Marketing Digital",
     "Mise en place et gestion pendant 1 mois de campagnes publicitaires pour un e-commerce. Budget publicitaire : 5000 MAD/mois.",
     2000, 30),
]

GIGS = [
    ("Création de site web React/Next.js", "Developpement Web",
     "Je développe votre site web ou landing page avec React ou Next.js. Design moderne, responsive et optimisé pour les performances. Inclus : déploiement Vercel.",
     "React, Next.js, Tailwind CSS, Vercel", 800, 5,
     [{"label": "SEO avancé", "description": "Optimisation SEO complète + sitemap + meta tags", "price": 300},
      {"label": "Formulaire de contact", "description": "Intégration formulaire + envoi email", "price": 150}]),
    ("Maquettes UI/UX Figma", "Design & UI/UX",
     "Je crée vos maquettes UI/UX professionnelles sur Figma. De l'idée au prototype cliquable. Style moderne, dark ou light selon votre besoin.",
     "Figma, UI Design, Prototypage, UX Research", 600, 4,
     [{"label": "Prototype interactif", "description": "Animations et transitions entre écrans", "price": 250},
      {"label": "Design system complet", "description": "Composants réutilisables + documentation", "price": 400}]),
    ("Script Python & automatisation", "Data & IA",
     "Développement de scripts Python pour automatiser vos tâches répétitives : scraping, traitement de données, rapports automatiques, intégrations API.",
     "Python, Pandas, BeautifulSoup, Selenium", 500, 3,
     [{"label": "Dashboard Streamlit", "description": "Visualisation interactive des résultats", "price": 350},
      {"label": "Rapport PDF automatique", "description": "Export PDF généré automatiquement", "price": 200}]),
    ("Application Flutter iOS/Android", "Mobile",
     "Développement d'applications mobiles cross-platform avec Flutter. Une seule base de code pour iOS et Android. Firebase inclus.",
     "Flutter, Dart, Firebase, REST API", 1500, 14,
     [{"label": "Notifications push", "description": "Intégration FCM pour notifications", "price": 300},
      {"label": "Mode hors-ligne", "description": "Synchronisation locale avec SQLite", "price": 400}]),
    ("Rédaction articles SEO", "Redaction",
     "Rédaction d'articles de blog optimisés SEO en français ou darija. Recherche de mots-clés incluse. Ton adapté à votre audience.",
     "Rédaction, SEO, WordPress, Recherche", 200, 2,
     [{"label": "Pack 5 articles", "description": "5 articles de 1000 mots au lieu de 1", "price": 800},
      {"label": "Publication WordPress", "description": "Mise en ligne directement sur votre site", "price": 100}]),
    ("Logo & Identité Visuelle", "Design & UI/UX",
     "Création de logo professionnel + charte graphique complète. Fichiers vectoriels livrés. Révisions illimitées jusqu'à satisfaction.",
     "Illustrator, Photoshop, Branding, Logo", 700, 6,
     [{"label": "Carte de visite", "description": "Design carte de visite recto-verso", "price": 200},
      {"label": "Kit réseaux sociaux", "description": "Bannières et templates pour vos réseaux", "price": 300}]),
]


class Command(BaseCommand):
    help = 'Seed fake students, recruiters, missions and gigs for testing'

    def handle(self, *args, **options):
        password = make_password('test1234')
        categories = {c.name: c for c in Category.objects.all()}

        # ── Students ─────────────────────────────────────────
        student_users = []
        for full_name, username, city, school, field, skills, rate in STUDENTS:
            if User.objects.filter(username=username).exists():
                u = User.objects.get(username=username)
            else:
                parts = full_name.split(' ', 1)
                u = User.objects.create(
                    username=username,
                    email=f'{username}@test.stulance.app',
                    first_name=parts[0],
                    last_name=parts[1] if len(parts) > 1 else '',
                    password=password,
                    role='student',
                    is_active=True,
                )
                StudentProfile.objects.create(
                    user=u,
                    bio=f"Étudiant(e) en {field} passionné(e) par les nouvelles technologies. Disponible pour des missions freelance.",
                    city=city,
                    school=school,
                    field_of_study=field,
                    skills=skills,
                    hourly_rate=rate,
                    verification_status='verified',
                )
            student_users.append(u)
            self.stdout.write(f'  OK Student: {username}')

        # ── Recruiters ───────────────────────────────────────
        recruiter_users = []
        for company, username, contact_name, city, description in RECRUITERS:
            if User.objects.filter(username=username).exists():
                u = User.objects.get(username=username)
            else:
                parts = contact_name.split(' ', 1)
                u = User.objects.create(
                    username=username,
                    email=f'contact@{username}.ma',
                    first_name=parts[0],
                    last_name=parts[1] if len(parts) > 1 else '',
                    password=password,
                    role='client',
                    is_active=True,
                )
                ClientProfile.objects.create(
                    user=u,
                    company_name=company,
                    city=city,
                    bio=description,
                )
            recruiter_users.append(u)
            self.stdout.write(f'  OK Recruiter: {username} ({company})')

        # ── Missions ─────────────────────────────────────────
        for title, cat_name, description, budget, deadline in MISSIONS:
            if Mission.objects.filter(title=title).exists():
                self.stdout.write(f'  - Mission already exists: {title}')
                continue
            cat = categories.get(cat_name)
            client = random.choice(recruiter_users)
            Mission.objects.create(
                client=client,
                title=title,
                description=description,
                category=cat,
                skills_required='',
                budget=budget,
                deadline_days=deadline,
                status='open',
            )
            self.stdout.write(f'  OK Mission: {title}')

        # ── Gigs ─────────────────────────────────────────────
        for title, cat_name, description, skills, rate, delivery, extras in GIGS:
            if Gig.objects.filter(title=title).exists():
                self.stdout.write(f'  - Gig already exists: {title}')
                continue
            cat = categories.get(cat_name)
            student = random.choice(student_users)
            Gig.objects.create(
                student=student,
                title=title,
                description=description,
                category=cat,
                skills=skills,
                base_rate=rate,
                delivery_days=delivery,
                extras=extras,
                is_active=True,
                status='approved',
            )
            self.stdout.write(f'  OK Gig: {title}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {len(STUDENTS)} students, {len(RECRUITERS)} recruiters, '
            f'{len(MISSIONS)} missions, {len(GIGS)} gigs created.'
        ))
