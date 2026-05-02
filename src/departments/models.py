from django.db import models
from django.conf import settings

class Department(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    
    dept_code = models.CharField(max_length=20, unique=True, verbose_name="Department Code")
    dept_name = models.CharField(max_length=100, verbose_name="Department Name")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    dept_head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'supervisor'},
        related_name='headed_departments',
        verbose_name="Supervisor"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['dept_name']

    def __str__(self):
        return f"{self.dept_name} ({self.dept_code})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('department-detail', kwargs={'pk': self.pk})
