from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Mission, Application, Review, Submission


class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['title', 'description', 'category', 'skills_required', 'budget', 'deadline_days']
        labels = {
            'title': _('Mission Title'),
            'description': _('Description'),
            'category': _('Category'),
            'skills_required': _('Required Skills'),
            'budget': _('Budget (MAD)'),
            'deadline_days': _('Deadline (days)'),
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g. Build a landing page for my startup'),
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('Describe the mission in detail — deliverables, context, expectations…'),
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'skills_required': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g. Python, Django, React — separate with commas'),
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '500',
                'min': '0',
            }),
            'deadline_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '7',
                'min': '1',
            }),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'proposed_budget', 'proposed_days', 'attachment']
        labels = {
            'cover_letter': _('Cover Letter'),
            'proposed_budget': _('Your Proposed Budget (MAD)'),
            'proposed_days': _('Your Proposed Timeline (days)'),
            'attachment': _('Supporting Document (optional)'),
        }
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 7,
                'placeholder': _('Introduce yourself and explain why you are the ideal candidate for this mission…'),
            }),
            'proposed_budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Leave blank to accept the posted budget'),
                'min': '0',
            }),
            'proposed_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Leave blank to accept the posted timeline'),
                'min': '1',
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.zip,.png,.jpg,.jpeg',
            }),
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
