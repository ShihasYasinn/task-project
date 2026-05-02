from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'client', 'service', 'status', 'friendly_name', 'assignee', 
            'start_date', 'end_date', 'is_recurring', 'repeat_every', 'period', 'recurrence_end_date'
        ]
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'friendly_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a friendly display name'}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'repeat_every': forms.NumberInput(attrs={'class': 'form-control'}),
            'period': forms.Select(attrs={'class': 'form-select'}),
            'recurrence_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_recurring = cleaned_data.get('is_recurring')
        recurrence_end_date = cleaned_data.get('recurrence_end_date')

        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', "End date cannot be before start date.")

        if is_recurring:
            if not recurrence_end_date:
                self.add_error('recurrence_end_date', "Recurrence end date is required for recurring projects.")
            elif start_date and recurrence_end_date < start_date:
                self.add_error('recurrence_end_date', "Recurrence end date cannot be before start date.")
            
            # If the user intended end_date to be the final end date, it should probably be recurrence_end_date.
            # But we'll let them have long instances if they really want, as long as it's valid.
        
        return cleaned_data
