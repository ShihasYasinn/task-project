from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_name', 'dept_code', 'dept_head', 'created_at')
    search_fields = ('dept_name', 'dept_code')
    list_filter = ('dept_head',)
