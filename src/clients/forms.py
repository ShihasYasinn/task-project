from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_code', 'name', 'surname', 'friendly_name', 'email', 'phone', 'company', 'address', 'status', 'entity_type']
        widgets = {
            'client_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CLT-101'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Legal Name of Entity'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Legal Last Name'}),
            'friendly_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred Display Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'primary@contact.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'International Format (e.g. +1...)'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent Organization'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Street Address, City, Region, Zip', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'entity_type': forms.Select(attrs={'class': 'form-select'}),
        }
