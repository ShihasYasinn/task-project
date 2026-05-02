from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'task_code', 'title', 'priority', 'assigned_days', 
            'days_before_project_end', 'start_date', 'end_date',
            'assignee', 'description', 'status'
        ]
        widgets = {
            'task_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task code'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'assigned_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'days_before_project_end': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task description', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['priority'].required = False
        self.fields['assigned_days'].required = False
        self.fields['days_before_project_end'].required = False

class ServiceTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'task_code', 'title', 'priority', 'assigned_days', 
            'days_before_project_end', 'assignee', 'description'
        ]
        widgets = {
            'task_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task code'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'assigned_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'days_before_project_end': forms.NumberInput(attrs={'class': 'form-control'}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task description', 'rows': 3}),
        }
