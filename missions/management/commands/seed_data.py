from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import StudentProfile, ClientProfile
from missions.models import Category, Mission
from gigs.models import Gig
import random

User = get_user_model()

CATEGORIES = [
    ('Développement Web', 'fa-code'),
    ('Design & UI/UX', 'fa-pen-nib'),
    ('Mobile', 'fa-mobile-alt'),
    ('Data & IA', 'fa-brain'),
    ('Marketing Digital', 'fa-bullhorn'),
    ('Rédaction', 'fa-pen'),
    ('Traduction', 'fa-language'),
    ('Vidéo & Montage', 'fa-film'),
]

STUDENTS = [
    ('youssef_dev', 'Youssef', 'Amrani', 'Python, Django, React', 'Casablanca', 120, 'EMSI', 'Génie Logiciel'),
    ('sara_design', 'Sara', 'Belkadi', 'Figma, Adobe XD, Illustrator', 'Rabat', 100, 'ENSIAS', 'Design'),
    ('omar_mobile', 'Omar', 'Tazi', 'Flutter, Dart, Firebase', 'Marrakech', 90, 'FST', 'Informatique'),
    ('hiba_data', 'Hiba', 'Moussaoui', 'Python, TensorFlow, Pandas', 'Casablanca', 150, 'EMSI', 'Data Science'),
    ('amine_fullstack', 'Amine', 'Rachidi', 'Vue.js, Node.js, MongoDB', 'Fès', 110, 'ENSA', 'Génie Informatique'),
]

RECRUITERS = [
    ('techcorp_ma', 'Karim', 'Benjelloun', 'TechCorp Maroc', 'company', 'Casablanca', 'Développement logiciel'),
    ('startup_io', 'Nadia', 'Chraibi', 'StartupIO', 'company', 'Rabat', 'SaaS & Produit'),
    ('freelance_rania', 'Rania', 'Lahlou', '', 'individual', 'Casablanca', 'Design & Branding'),
    ('atlas_agency', 'Mehdi', 'Alaoui', 'Atlas Digital Agency', 'company', 'Marrakech', 'Marketing Digital'),
]

MISSIONS = [
    ('Développement d\'une API REST Django', 'Nous cherchons un étudiant pour développer une API REST complète avec Django REST Framework pour notre application mobile.', 'Développement Web', 'Python, Django, REST API', 3000, 21),
    ('Création d\'une maquette UI pour app mobile', 'Concevoir les écrans d\'une application mobile de livraison avec Figma. Livrables : 20 écrans + guide de style.', 'Design & UI/UX', 'Figma, UI/UX, Mobile', 1500, 14),
    ('Application Flutter e-commerce', 'Développer une app Flutter connectée à Firebase avec panier, paiement et notifications push.', 'Mobile', 'Flutter, Firebase, Dart', 4000, 30),
    ('Tableau de bord analytique avec Python', 'Créer un dashboard interactif avec Dash/Plotly pour visualiser les données de ventes de notre boutique.', 'Data & IA', 'Python, Pandas, Plotly', 2500, 20),
    ('Gestion des réseaux sociaux', 'Animation de nos pages Instagram, Facebook et LinkedIn pendant 3 mois. Création de contenu incluse.', 'Marketing Digital', 'Social Media, Canva, Copywriting', 1200, 90),
    ('Développement site WordPress', 'Créer un site vitrine professionnel sous WordPress avec thème personnalisé et formulaire de contact.', 'Développement Web', 'WordPress, PHP, CSS', 800, 10),
    ('Traduction documents FR → AR', 'Traduire 30 pages de documentation technique du français vers l\'arabe. Domaine : logistique.', 'Traduction', 'Arabe, Français, Traduction technique', 600, 7),
    ('Montage vidéo promotionnel', 'Monter une vidéo de 2 minutes pour notre lancement produit. Fourniture des rushes et musique.', 'Vidéo & Montage', 'Premiere Pro, After Effects', 900, 5),
]

GIGS = [
    ('Je crée votre site web Django en 7 jours', 'Site web complet avec Django, base de données, authentification et déploiement sur VPS.', 'Développement Web', 'Django, Python, PostgreSQL', 1500, 7),
    ('Design Figma de votre app mobile', 'Maquette complète d\'une application mobile : wireframes, UI haute fidélité et prototype interactif.', 'Design & UI/UX', 'Figma, Prototypage, UI Design', 800, 5),
    ('Application Flutter cross-platform', 'Développement d\'une app Flutter fonctionnelle sur iOS et Android avec Firebase intégré.', 'Mobile', 'Flutter, Firebase, Dart', 3000, 21),
    ('Analyse de données et visualisation', 'Nettoyage, analyse et visualisation de vos données avec Python. Rapport PDF inclus.', 'Data & IA', 'Python, Pandas, Matplotlib', 700, 3),
    ('Rédaction d\'articles SEO', 'Rédaction de 5 articles optimisés SEO de 800 mots dans votre domaine.', 'Rédaction', 'SEO, Copywriting, WordPress', 400, 4),
]


class Command(BaseCommand):
    help = 'Seed the database with fake data for development'

    def handle(self, *args, **options):
        self.stdout.write('Seeding categories...')
        categories = {}
        for name, icon in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'icon': icon})
            categories[name] = cat

        self.stdout.write('Seeding students...')
        students = []
        for username, first, last, skills, city, rate, school, field in STUDENTS:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@stulance.ma',
                    password='stulance123',
                    first_name=first,
                    last_name=last,
                    role='student',
                    phone=f'06{random.randint(10000000, 99999999)}',
                )
                StudentProfile.objects.create(
                    user=user,
                    bio=f'Étudiant passionné en {field} à {school}. Disponible pour des missions freelance.',
                    skills=skills,
                    city=city,
                    hourly_rate=rate,
                    school=school,
                    field_of_study=field,
                    verification_status='verified',
                    average_rating=round(random.uniform(3.5, 5.0), 1),
                    total_missions=random.randint(1, 10),
                )
            students.append(user)

        self.stdout.write('Seeding recruiters...')
        recruiters = []
        for username, first, last, company, ctype, city, field in RECRUITERS:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@stulance.ma',
                    password='stulance123',
                    first_name=first,
                    last_name=last,
                    role='client',
                    phone=f'05{random.randint(10000000, 99999999)}',
                )
                ClientProfile.objects.create(
                    user=user,
                    company_name=company,
                    client_type=ctype,
                    bio=f'Entreprise active dans le domaine {field} basée à {city}.',
                    city=city,
                    main_field=field,
                    average_rating=round(random.uniform(3.8, 5.0), 1),
                )
            recruiters.append(user)

        self.stdout.write('Seeding missions...')
        for title, desc, cat_name, skills, budget, days in MISSIONS:
            if not Mission.objects.filter(title=title).exists():
                Mission.objects.create(
                    client=random.choice(recruiters),
                    title=title,
                    description=desc,
                    category=categories[cat_name],
                    skills_required=skills,
                    budget=budget,
                    deadline_days=days,
                    status=random.choice(['open', 'open', 'open', 'in_progress']),
                )

        self.stdout.write('Seeding gigs...')
        student_iter = students.copy()
        random.shuffle(student_iter)
        for i, (title, desc, cat_name, skills, rate, days) in enumerate(GIGS):
            if not Gig.objects.filter(title=title).exists():
                Gig.objects.create(
                    student=student_iter[i % len(student_iter)],
                    title=title,
                    description=desc,
                    category=categories[cat_name],
                    skills=skills,
                    base_rate=rate,
                    delivery_days=days,
                    status='approved',
                    is_active=True,
                )

        self.stdout.write(self.style.SUCCESS(
            f'Done! {len(students)} students, {len(recruiters)} recruiters, '
            f'{Mission.objects.count()} missions, {Gig.objects.count()} gigs.'
        ))
