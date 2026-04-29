from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_code', 'dept_name', 'dept_head']
        widgets = {
            'dept_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. IT-01'}),
            'dept_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Information Technology'}),
            'dept_head': forms.Select(attrs={'class': 'form-select'}),
        }
