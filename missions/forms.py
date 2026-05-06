from django import forms
from .models import Mission, Application, Review, Submission


class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['title', 'description', 'category', 'skills_required', 'budget', 'deadline_days']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'skills_required': forms.TextInput(attrs={'placeholder': 'ex: Python, Django, React'}),
            'budget': forms.NumberInput(attrs={'placeholder': 'Budget en MAD'}),
            'deadline_days': forms.NumberInput(attrs={'placeholder': 'Nombre de jours'}),
        }
        labels = {
            'title': 'Titre de la mission',
            'description': 'Description',
            'category': 'Categorie',
            'skills_required': 'Competences requises',
            'budget': 'Budget (MAD)',
            'deadline_days': 'Delai (jours)',
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Presentez-vous et expliquez pourquoi vous etes le candidat ideal...'}),
        }
        labels = {
            'cover_letter': 'Lettre de motivation',
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file', 'link', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Decrivez ce que vous livrez...'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
        }
        labels = {
            'file': 'Fichier (optionnel)',
            'link': 'Lien (optionnel)',
            'message': 'Message',
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('file') and not cleaned.get('link'):
            raise forms.ValidationError('Fournissez au moins un fichier ou un lien.')
        return cleaned


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.RadioSelect(),
        }
        labels = {
            'rating': 'Note (1 a 5)',
            'comment': 'Commentaire',
        }
