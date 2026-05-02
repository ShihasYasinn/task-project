from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client-list'),
    path('add/', views.client_create, name='client-add'),
    path('<int:pk>/', views.client_detail, name='client-detail'),
    path('<int:pk>/edit/', views.client_update, name='client-update'),
    path('<int:pk>/delete/', views.client_delete, name='client-delete'),
]
