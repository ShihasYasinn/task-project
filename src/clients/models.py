from django.db import models
from django.urls import reverse

class Client(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    ENTITY_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('partnership', 'Partnership'),
        ('other', 'Other'),
    )

    client_code = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Client Code")
    name = models.CharField(max_length=255, verbose_name="Name")
    surname = models.CharField(max_length=255, blank=True, null=True, verbose_name="Surname")
    friendly_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Friendly Name")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES, default='company', verbose_name="Entity Type")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.name} {self.surname if self.surname else ''} ({self.client_code})"

    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'pk': self.pk})
