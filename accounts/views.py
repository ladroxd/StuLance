from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, StudentProfile, ClientProfile, PortfolioProject
from .forms import StudentRegisterForm, ClientRegisterForm, StudentProfileForm, ClientProfileForm, PortfolioProjectForm


def onboarding(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'student':
            return redirect('register_student')
        elif role == 'recruiter':
            return redirect('register_client')
    return render(request, 'accounts/onboarding.html')


def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte etudiant cree. En attente de verification.')
            return redirect('dashboard')
    else:
        form = StudentRegisterForm()
    return render(request, 'accounts/register_student.html', {'form': form})


def register_client(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte client cree avec succes.')
            return redirect('dashboard')
    else:
        form = ClientRegisterForm()
    return render(request, 'accounts/register_client.html', {'form': form})


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


@login_required
def student_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'accounts/student_profile.html', {'profile': profile})


def student_profile_detail(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    return render(request, 'accounts/student_profile_detail.html', {'profile': profile})


def client_profile_detail(request, pk):
    profile = get_object_or_404(ClientProfile, pk=pk)
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
