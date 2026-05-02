from django.db import models
from django.urls import reverse
from django.conf import settings

class Service(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    service_code = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Service Code")
    name = models.CharField(max_length=100, verbose_name="Name of Service")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    description = models.TextField(blank=True, null=True, verbose_name="Service Description")
    department = models.ForeignKey(
        'departments.Department', 
        on_delete=models.CASCADE, 
        null=True,
        blank=True,
        related_name='services',
        verbose_name="Department"
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_services',
        verbose_name="Assignee"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.service_code})"

    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'pk': self.pk})
