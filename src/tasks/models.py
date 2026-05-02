from django.db import models
from django.conf import settings

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in-progress', 'In Progress'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
        ('completed', 'Completed'),
    )

    # Relationships
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='service_tasks', null=True, blank=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    
    # Core Fields
    task_code = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Timing & Scheduling
    assigned_days = models.IntegerField(default=0)
    days_before_project_end = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    # Assignments
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    agents = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='agent_tasks')
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='collaborator_tasks')
    
    description = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.task_code} - {self.title}"
