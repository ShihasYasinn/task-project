from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

class Project(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    
    PERIOD_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )

    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='projects')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='projects')
    project_code = models.CharField(max_length=50, unique=True)
    friendly_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_projects')
    
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    
    # Recurrence fields
    is_recurring = models.BooleanField(default=False)
    repeat_every = models.IntegerField(default=1, null=True, blank=True)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly', null=True, blank=True)
    recurrence_end_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.project_code:
            # Generate project code: SVC-CLT-YYYYMM-XXX
            import datetime
            now = datetime.datetime.now()
            date_str = now.strftime('%Y%m')
            service_code = self.service.service_code if self.service else 'SRV'
            client_code = self.client.client_code if self.client else 'CLT'
            
            # Count existing projects for this client/service/month
            count = Project.objects.filter(
                client=self.client, 
                service=self.service,
                created_at__year=now.year,
                created_at__month=now.month
            ).count() + 1
            
            self.project_code = f"{service_code}-{client_code}-{date_str}-{count:03d}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_code} - {self.friendly_name if self.friendly_name else self.service.name}"

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})
