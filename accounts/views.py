from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, StudentProfile, ClientProfile, PortfolioProject
from .forms import StudentRegisterForm, ClientRegisterForm, StudentProfileForm, ClientProfileForm, PortfolioProjectForm


PREDEFINED_SKILLS = [
    'Web Development', 'Mobile Development', 'UI/UX Design', 'Graphic Design',
    'Data Analysis', 'ML / AI', 'Python', 'JavaScript', 'React.js', 'Vue.js',
    'Node.js', 'Laravel', 'Django', 'Flutter', 'DevOps', 'Cybersecurity',
    '3D Modeling', 'Video Editing', 'Content Writing', 'SEO',
    'Social Media Marketing', 'Accounting', 'Translation', 'TypeScript',
]

WORK_TYPES = ['Freelance', 'Intern', 'Full Time', 'Part Time', 'Remote']

MAIN_FIELDS = [
    ('technology', 'Technology & IT'),
    ('business', 'Business & Finance'),
    ('engineering', 'Engineering & Mechanics'),
    ('design', 'Design & Creative'),
    ('marketing', 'Marketing & Communication'),
    ('education', 'Education & Research'),
    ('healthcare', 'Healthcare'),
    ('legal', 'Legal & Consulting'),
]


def _ob_clear(request):
    for key in ('ob_step', 'ob_role', 'ob_data'):
        request.session.pop(key, None)


def _create_student_account(data):
    user = User(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        role=User.ROLE_STUDENT,
        password=make_password(data['password']),
    )
    user.save()
    hourly_rate = None
    if data.get('hourly_rate'):
        try:
            hourly_rate = float(data['hourly_rate'])
        except (ValueError, TypeError):
            pass
    StudentProfile.objects.create(
        user=user,
        bio=data.get('bio', ''),
        school=data.get('university', ''),
        city=data.get('city', ''),
        skills=', '.join(data.get('skills', [])),
        hourly_rate=hourly_rate,
    )
    return user


def _create_recruiter_account(data):
    user = User(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        role=User.ROLE_CLIENT,
        password=make_password(data['password']),
    )
    user.save()
    ClientProfile.objects.create(
        user=user,
        company_name=data.get('company_name', ''),
        bio=data.get('company_description', ''),
        city=data.get('city', ''),
        work_types=', '.join(data.get('work_types', [])),
        main_field=data.get('main_field', ''),
        client_type=ClientProfile.TYPE_COMPANY,
    )
    return user


def onboarding(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    step = request.session.get('ob_step', 1)
    role = request.session.get('ob_role', None)
    ob_data = request.session.get('ob_data', {})
    errors = {}

    if request.method == 'POST':
        action = request.POST.get('action', 'next')
        posted_step = int(request.POST.get('step', '1'))

        if action == 'back':
            step = max(1, posted_step - 1)
            request.session['ob_step'] = step

        elif posted_step == 1:
            role = request.POST.get('role', '').strip()
            if role in ('student', 'recruiter'):
                request.session['ob_role'] = role
                request.session['ob_step'] = 2
                request.session['ob_data'] = {}
                ob_data = {}
                step = 2
            else:
                errors['role'] = 'Please select a role.'

        elif posted_step == 2:
            if role == 'student':
                f = {
                    'username': request.POST.get('username', '').strip(),
                    'first_name': request.POST.get('first_name', '').strip(),
                    'last_name': request.POST.get('last_name', '').strip(),
                    'email': request.POST.get('email', '').strip(),
                    'university': request.POST.get('university', '').strip(),
                    'city': request.POST.get('city', '').strip(),
                    'bio': request.POST.get('bio', '').strip(),
                    'password1': request.POST.get('password1', ''),
                    'password2': request.POST.get('password2', ''),
                }
                if not f['username']:
                    errors['username'] = 'Username is required.'
                elif User.objects.filter(username=f['username']).exists():
                    errors['username'] = 'Username already taken.'
                if not f['first_name']:
                    errors['first_name'] = 'First name is required.'
                if not f['last_name']:
                    errors['last_name'] = 'Last name is required.'
                if not f['email']:
                    errors['email'] = 'Email is required.'
                elif User.objects.filter(email=f['email']).exists():
                    errors['email'] = 'Email already in use.'
                if not f['university']:
                    errors['university'] = 'University is required.'
                if not f['city']:
                    errors['city'] = 'City is required.'
                if not f['password1']:
                    errors['password1'] = 'Password is required.'
                elif len(f['password1']) < 8:
                    errors['password1'] = 'Password must be at least 8 characters.'
                elif f['password1'] != f['password2']:
                    errors['password2'] = 'Passwords do not match.'
                if not request.POST.get('tos_accepted'):
                    errors['tos_accepted'] = 'You must accept the Terms of Service.'
                if not errors:
                    ob_data.update({k: v for k, v in f.items() if k not in ('password1', 'password2')})
                    ob_data['password'] = f['password1']
                    request.session['ob_data'] = ob_data
                    request.session['ob_step'] = 3
                    step = 3
                else:
                    ob_data.update({k: v for k, v in f.items() if k not in ('password1', 'password2')})

            else:  # recruiter
                f = {
                    'full_name': request.POST.get('full_name', '').strip(),
                    'email': request.POST.get('email', '').strip(),
                    'company_name': request.POST.get('company_name', '').strip(),
                    'city': request.POST.get('city', '').strip(),
                    'company_description': request.POST.get('company_description', '').strip(),
                    'password1': request.POST.get('password1', ''),
                    'password2': request.POST.get('password2', ''),
                }
                if not f['full_name']:
                    errors['full_name'] = 'Full name is required.'
                if not f['email']:
                    errors['email'] = 'Email is required.'
                elif User.objects.filter(email=f['email']).exists():
                    errors['email'] = 'Email already in use.'
                if not f['company_name']:
                    errors['company_name'] = 'Company name is required.'
                if not f['city']:
                    errors['city'] = 'City is required.'
                if not f['password1']:
                    errors['password1'] = 'Password is required.'
                elif len(f['password1']) < 8:
                    errors['password1'] = 'Password must be at least 8 characters.'
                elif f['password1'] != f['password2']:
                    errors['password2'] = 'Passwords do not match.'
                if not request.POST.get('tos_accepted'):
                    errors['tos_accepted'] = 'You must accept the Terms of Service.'
                if not errors:
                    base = f['company_name'].lower().replace(' ', '_')[:20]
                    username = base
                    n = 1
                    while User.objects.filter(username=username).exists():
                        username = f'{base}{n}'
                        n += 1
                    parts = f['full_name'].split(' ', 1)
                    ob_data.update({
                        'username': username,
                        'first_name': parts[0],
                        'last_name': parts[1] if len(parts) > 1 else '',
                        'email': f['email'],
                        'company_name': f['company_name'],
                        'city': f['city'],
                        'company_description': f['company_description'],
                        'password': f['password1'],
                        'full_name': f['full_name'],
                    })
                    request.session['ob_data'] = ob_data
                    request.session['ob_step'] = 3
                    step = 3
                else:
                    ob_data.update({k: v for k, v in f.items() if k not in ('password1', 'password2')})

        elif posted_step == 3:
            if role == 'student':
                selected = request.POST.getlist('skills')
                custom_raw = request.POST.get('custom_skills', '').strip()
                hourly_rate = request.POST.get('hourly_rate', '').strip()
                all_skills = selected + [s.strip() for s in custom_raw.split(',') if s.strip()]
                ob_data.update({'skills': all_skills, 'custom_skills': custom_raw, 'hourly_rate': hourly_rate})
                request.session['ob_data'] = ob_data
                request.session['ob_step'] = 4
                step = 4
            else:
                work_types = request.POST.getlist('work_types')
                main_field = request.POST.get('main_field', '').strip()
                if not work_types:
                    errors['work_types'] = 'Select at least one work type.'
                if not main_field:
                    errors['main_field'] = 'Please select your main field.'
                if not errors:
                    ob_data.update({'work_types': work_types, 'main_field': main_field})
                    try:
                        user = _create_recruiter_account(ob_data)
                        login(request, user)
                        _ob_clear(request)
                        messages.success(request, 'Welcome to StuLance!')
                        return redirect('dashboard')
                    except Exception as e:
                        errors['general'] = f'Account creation failed: {str(e)}'

        elif posted_step == 4:
            try:
                if role == 'student':
                    user = _create_student_account(ob_data)
                else:
                    user = _create_recruiter_account(ob_data)
                login(request, user)
                _ob_clear(request)
                if role == 'student':
                    messages.success(request, 'Welcome to StuLance! Your account is pending verification.')
                else:
                    messages.success(request, 'Welcome to StuLance!')
                return redirect('dashboard')
            except Exception as e:
                errors['general'] = f'Account creation failed: {str(e)}'

        request.session.modified = True

    context = {
        'step': step,
        'role': role,
        'ob_data': ob_data,
        'errors': errors,
        'predefined_skills': PREDEFINED_SKILLS,
        'work_types_list': WORK_TYPES,
        'main_fields': MAIN_FIELDS,
    }
    return render(request, 'accounts/onboarding.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))
        messages.error(request, 'Identifiants incorrects.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def onboarding_exit(request):
    _ob_clear(request)
    return redirect('home')


@login_required
def student_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'accounts/student_profile.html', {'profile': profile})


def student_profile_detail(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    return render(request, 'accounts/student_profile_detail.html', {'profile': profile})


def client_profile_detail(request, pk):
    profile = get_object_or_404(ClientProfile, user__pk=pk)
    return render(request, 'accounts/client_profile_detail.html', {'profile': profile})


@login_required
def edit_student_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis a jour.')
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def edit_client_profile(request):
    profile = get_object_or_404(ClientProfile, user=request.user)
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis a jour.')
            return redirect('dashboard')
    else:
        form = ClientProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def add_portfolio_project(request):
    if request.method == 'POST':
        form = PortfolioProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = request.user.student_profile
            project.save()
            messages.success(request, 'Projet ajoute au portfolio.')
            return redirect('student_profile')
    else:
        form = PortfolioProjectForm()
    return render(request, 'accounts/portfolio_form.html', {'form': form})


@login_required
def delete_portfolio_project(request, pk):
    project = get_object_or_404(PortfolioProject, pk=pk, student=request.user.student_profile)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Projet supprime.')
    return redirect('student_profile')
