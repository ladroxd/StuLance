from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User, StudentProfile, ClientProfile, PortfolioProject


class StudentRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label=_('First Name'))
    last_name = forms.CharField(max_length=100, required=True, label=_('Last Name'))
    email = forms.EmailField(required=True, label=_('Email'))
    school = forms.CharField(max_length=200, required=True, label=_('School'))
    field_of_study = forms.CharField(max_length=200, required=True, label=_('Field of Study'))
    student_card = forms.FileField(required=True, label=_('Student Card'), help_text=_('Student card (PDF or image)'))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLE_STUDENT
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                school=self.cleaned_data['school'],
                field_of_study=self.cleaned_data['field_of_study'],
                student_card=self.cleaned_data['student_card'],
            )
        return user


class ClientRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label=_('First Name'))
    last_name = forms.CharField(max_length=100, required=True, label=_('Last Name'))
    email = forms.EmailField(required=True, label=_('Email'))
    client_type = forms.ChoiceField(choices=ClientProfile.TYPE_CHOICES, label=_('Client Type'))
    company_name = forms.CharField(max_length=200, required=False, label=_('Company Name'))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLE_CLIENT
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            ClientProfile.objects.create(
                user=user,
                client_type=self.cleaned_data['client_type'],
                company_name=self.cleaned_data.get('company_name', ''),
            )
        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['photo', 'bio', 'skills', 'github_url', 'linkedin_url', 'school', 'field_of_study', 'student_card']
        labels = {
            'photo': _('Photo'),
            'bio': _('Bio'),
            'skills': _('Skills'),
            'github_url': _('GitHub URL'),
            'linkedin_url': _('LinkedIn URL'),
            'school': _('School'),
            'field_of_study': _('Field of Study'),
            'student_card': _('Student Card'),
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.TextInput(attrs={'placeholder': _('e.g. Python, Django, React')}),
        }


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['photo', 'client_type', 'company_name', 'bio', 'website']
        labels = {
            'photo': _('Photo'),
            'client_type': _('Client Type'),
            'company_name': _('Company Name'),
            'bio': _('Bio'),
            'website': _('Website'),
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class PortfolioProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = ['title', 'description', 'url', 'image']
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'url': _('URL'),
            'image': _('Image'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
