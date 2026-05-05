from django import forms
from django.shortcuts import render, redirect

from missions.models import Mission, Category


def home(request):
    missions = Mission.objects.filter(status='open').order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'home.html', {'missions': missions, 'categories': categories})


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
