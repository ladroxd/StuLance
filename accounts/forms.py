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
            'photo': _('Profile Photo'),
            'bio': _('Bio'),
            'skills': _('Skills'),
            'github_url': _('GitHub URL'),
            'linkedin_url': _('LinkedIn URL'),
            'school': _('School / University'),
            'field_of_study': _('Field of Study'),
            'student_card': _('Student Card'),
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': _('Tell clients about yourself, your experience, and what you can offer…'),
            }),
            'skills': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g. Python, Django, React — separate with commas'),
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username',
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/username',
            }),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'student_card': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*,.pdf'}),
        }


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['photo', 'client_type', 'company_name', 'bio', 'website']
        labels = {
            'photo': _('Profile Photo'),
            'client_type': _('Client Type'),
            'company_name': _('Company / Organization Name'),
            'bio': _('About'),
            'website': _('Website'),
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': _('Tell students about your company and the kind of work you post…'),
            }),
            'client_type': forms.Select(attrs={'class': 'form-select'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourcompany.com',
            }),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class PortfolioProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = ['title', 'description', 'url', 'image']
        labels = {
            'title': _('Project Title'),
            'description': _('Description'),
            'url': _('Project URL'),
            'image': _('Preview Image'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('e.g. E-commerce Dashboard')}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': _('What did you build? What technologies did you use?'),
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/you/project',
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
