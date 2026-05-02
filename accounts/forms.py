from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, ClientProfile, PortfolioProject


class StudentRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    school = forms.CharField(max_length=200, required=True)
    field_of_study = forms.CharField(max_length=200, required=True)
    student_card = forms.FileField(required=True, help_text='Carte etudiante (PDF ou image)')

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
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    client_type = forms.ChoiceField(choices=ClientProfile.TYPE_CHOICES)
    company_name = forms.CharField(max_length=200, required=False)

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
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.TextInput(attrs={'placeholder': 'ex: Python, Django, React'}),
        }


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['photo', 'client_type', 'company_name', 'bio', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class PortfolioProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = ['title', 'description', 'url', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
