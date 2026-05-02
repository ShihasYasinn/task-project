from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project-list'),
    path('add/', views.project_create, name='project-add'),
    path('<int:pk>/', views.project_detail, name='project-detail'),
    path('<int:pk>/edit/', views.project_update, name='project-update'),
    path('<int:pk>/delete/', views.project_delete, name='project-delete'),
]
