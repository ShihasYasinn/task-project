from django.db import models
from django.conf import settings

class Department(models.Model):
    dept_code = models.CharField(max_length=20, unique=True, verbose_name="Department Code")
    dept_name = models.CharField(max_length=100, verbose_name="Department Name")
    dept_head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'supervisor'},
        related_name='headed_departments',
        verbose_name="Department Head"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['dept_name']

    def __str__(self):
        return f"{self.dept_name} ({self.dept_code})"
