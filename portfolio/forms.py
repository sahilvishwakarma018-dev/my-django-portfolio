from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'attachment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your.email@example.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Your message here...',
                'rows': 5
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': '.pdf,.doc,.docx,.txt'
            })
        }
