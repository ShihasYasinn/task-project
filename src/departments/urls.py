from django.urls import path
from . import views

urlpatterns = [
    path('', views.department_list, name='department-list'),
    path('add/', views.department_create, name='department-add'),
    path('<int:pk>/', views.department_detail, name='department-detail'),
    path('<int:pk>/edit/', views.department_update, name='department-update'),
    path('<int:pk>/delete/', views.department_delete, name='department-delete'),
]
