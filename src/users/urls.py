from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user-list'),
    path('add/', views.user_create, name='user-add'),
    path('<int:pk>/', views.user_detail, name='user-detail'),
    path('<int:pk>/edit/', views.user_update, name='user-update'),
    path('<int:pk>/delete/', views.user_delete, name='user-delete'),
]
