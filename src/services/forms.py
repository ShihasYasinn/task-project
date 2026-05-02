from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_code', 'name', 'department', 'assignee', 'status', 'description']
        widgets = {
            'service_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unique ID (e.g. SVC-100)', 'required': 'required'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descriptive Service Name', 'required': 'required'}),
            'department': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'assignee': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'status': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide a detailed overview of the service...', 'rows': 4}),
        }
