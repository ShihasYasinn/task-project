from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('users/', include('users.urls')),
    path('departments/', include('departments.urls')),
    path('services/', include('services.urls')),
    path('clients/', include('clients.urls')),
    path('projects/', include('projects.urls')),
    path('tasks/', include('tasks.urls')),
]
