import json
from django import forms
from django.shortcuts import render, redirect
from django.utils.text import Truncator

from missions.models import Mission, Category
from missions.utils import get_all_categories


def home(request):
    missions_qs = Mission.objects.filter(status='open').select_related('client', 'client__client_profile', 'category').order_by('-created_at')[:6]
    categories = get_all_categories()

    missions_json = json.dumps([
        {
            'pk': m.pk,
            'title': m.title,
            'description': Truncator(m.description).words(20),
            'category': str(m.category) if m.category else '',
            'budget': float(m.budget),
            'deadline_days': m.deadline_days,
            'applications_count': m.applications.count(),
            'skills': (m.skills_required or '').split(',')[:3] if m.skills_required else [],
            'company_name': (
                m.client.client_profile.company_name
                or m.client.get_full_name()
                or m.client.username
            ) if hasattr(m.client, 'client_profile') else m.client.username,
        }
        for m in missions_qs
    ], ensure_ascii=False)

    return render(request, 'home.html', {
        'missions': missions_qs,
        'categories': categories,
        'missions_json': missions_json,
    })


def tos(request):
    return render(request, 'pages/tos.html')


def help_center(request):
    return render(request, 'pages/help.html')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    subject = forms.CharField(max_length=80, required=False)
    message = forms.CharField(widget=forms.Textarea)


def email_us(request):
    return render(request, 'pages/email_us.html')


def blog(request):
    posts = [
        {
            "slug": "freelancing-as-a-student-in-morocco",
            "title": "Freelancing as a Student in Morocco: Where to Start",
            "excerpt": "Breaking into the freelance market while studying can feel overwhelming. Here's a practical roadmap built for Moroccan students.",
            "date": "April 28, 2026",
            "read_time": "5 min read",
            "category": "Career",
            "icon": "bi-mortarboard",
            "color": "#7c3aed",
            "body": [
                ("The opportunity is real", "Morocco has a growing startup and SME ecosystem hungry for affordable digital talent. As a student, your skills in web development, design, data, or marketing are exactly what these companies need — and StuLance is the bridge."),
                ("Start with what you know", "Don't wait until you feel 'ready'. Post a gig around your strongest skill — even if it's a single technology. Your first mission doesn't have to be perfect; it has to be completed."),
                ("Build your profile first", "Clients look at your profile before your proposal. Add a clear photo, write a short bio that mentions your school and field, and list your top 5 skills. A complete profile gets 3× more views."),
                ("Price smartly", "Start at a rate that reflects effort, not market average. 150–300 MAD per hour is a reasonable range for a student with a portfolio. Raise it after your first 3 reviews."),
            ],
        },
        {
            "slug": "how-to-write-a-winning-mission-proposal",
            "title": "How to Write a Winning Mission Proposal",
            "excerpt": "Most proposals are copy-paste noise. Learn how to write one that actually gets a response — in under 150 words.",
            "date": "May 1, 2026",
            "read_time": "4 min read",
            "category": "Tips",
            "icon": "bi-pencil-square",
            "color": "#0ea5e9",
            "body": [
                ("Read the mission twice", "Clients can tell immediately if you didn't read their brief. Reference something specific from it in your first sentence — that alone puts you in the top 10%."),
                ("Lead with the solution", "Don't start with 'I am a student at…'. Start with 'I'd solve this by…'. Show you already have a plan before they've paid you anything."),
                ("Keep it short", "The ideal proposal is 3 paragraphs: your approach, one relevant past project (or course), and a clear timeline + price. Anything longer gets skimmed."),
                ("End with a question", "A question like 'Would a 7-day delivery work for your timeline?' turns a one-way pitch into a conversation and doubles your reply rate."),
            ],
        },
        {
            "slug": "top-skills-in-demand-2026",
            "title": "Top Skills Clients Are Looking For in 2026",
            "excerpt": "An analysis of StuLance mission postings reveals which technical and creative skills are most requested this year.",
            "date": "May 3, 2026",
            "read_time": "3 min read",
            "category": "Trends",
            "icon": "bi-bar-chart-line",
            "color": "#10b981",
            "body": [
                ("Web & Mobile Development", "React, Django, Flutter — full-stack and mobile missions make up over 40% of posts. If you can build and deploy an MVP, you will never run out of work."),
                ("Data & AI", "Data cleaning, dashboards, and simple ML scripts are in high demand from SMEs that can't afford a full data team. Python + Pandas + a good chart library goes a long way."),
                ("UI/UX Design", "Figma prototypes and landing page redesigns are the easiest entry point for design students. Clients want something they can show investors — fast."),
                ("Digital Marketing & SEO", "Social media strategy, Google Ads setup, and basic SEO audits are requested constantly by small e-commerce businesses. Often overlooked by tech students."),
            ],
        },
        {
            "slug": "for-clients-how-to-post-a-great-mission",
            "title": "For Clients: How to Post a Mission That Attracts Talent",
            "excerpt": "A vague mission gets vague proposals. Here's how to write a brief that brings out the best student talent on StuLance.",
            "date": "May 5, 2026",
            "read_time": "4 min read",
            "category": "For Clients",
            "icon": "bi-briefcase",
            "color": "#f59e0b",
            "body": [
                ("Be specific about the output", "Instead of 'I need a website', write 'I need a 5-page responsive website in React with a contact form and deployed on Vercel'. Specificity attracts students who know exactly what to do."),
                ("Set a realistic budget", "Students are affordable but not free. A 2-week mission with real deliverables should be budgeted at 1,500–4,000 MAD depending on complexity. Underpaying filters out your best candidates."),
                ("List the skills you need", "Use the skills field. Students filter missions by their abilities. If you need 'Figma + Tailwind CSS', say so — the right person will find you."),
                ("Respond quickly", "The best students apply to multiple missions. If you take 5 days to respond, you've already lost them. Aim to review applications within 48 hours."),
            ],
        },
        {
            "slug": "building-a-portfolio-from-zero",
            "title": "Building a Portfolio From Zero While Still in School",
            "excerpt": "No clients yet? No problem. Here are five ways to build a credible portfolio before your first paid mission.",
            "date": "May 5, 2026",
            "read_time": "6 min read",
            "category": "Career",
            "icon": "bi-stars",
            "color": "#ec4899",
            "body": [
                ("Rebuild something you use", "Pick an app or website you use daily and redesign or rebuild a feature. It shows taste, initiative, and real-world context — more compelling than a school project."),
                ("Contribute to open source", "Even one merged pull request on a public GitHub repo is portfolio gold. Start with 'good first issue' labels on projects you've used."),
                ("Do one free mission strategically", "One free or heavily discounted mission for a real client — ideally an NGO, student club, or local business — gives you a case study with a real logo on it."),
                ("Document everything", "A README, a short Loom walkthrough, or a before/after screenshot turns a project into a story. Clients hire the story, not the code."),
                ("Use StuLance Gigs", "Post a gig on StuLance even before you have reviews. A clear description and a sample of your work is enough to start getting inquiries."),
            ],
        },
        {
            "slug": "stulance-platform-update-may-2026",
            "title": "Platform Update — May 2026: What's New on StuLance",
            "excerpt": "New features landed this month: glass mission cards, an improved profile page, and the early access blog.",
            "date": "May 5, 2026",
            "read_time": "2 min read",
            "category": "Updates",
            "icon": "bi-rocket-takeoff",
            "color": "#7c3aed",
            "body": [
                ("Glass Mission Cards", "The home page now shows featured missions with a new card design — category icons, skill tags, budget, and deadline at a glance."),
                ("Blog launched", "You're reading it. We'll post weekly content around freelancing, platform tips, and community stories from Moroccan students."),
                ("Student & Client profiles improved", "Profile pages now load faster and show cleaner skill and portfolio sections. More refinements are coming before our first traffic push."),
                ("Coming soon", "Client identity on mission cards, a work delivery/submission system, and SSE-based real-time messaging. Stay tuned."),
            ],
        },
    ]
    return render(request, 'pages/blog.html', {'posts': posts})


def contact(request):
    success = False
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # TODO: wire up email sending when EMAIL_BACKEND is configured
            success = True
            form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form, 'success': success})
