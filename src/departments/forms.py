from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_code', 'dept_name', 'status', 'dept_head']
        widgets = {
            'dept_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter department code'}),
            'dept_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter department name'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'dept_head': forms.Select(attrs={'class': 'form-select'}),
        }
