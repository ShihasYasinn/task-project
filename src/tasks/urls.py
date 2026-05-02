from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/update/', views.task_update, name='task-update'),
    path('<int:pk>/delete/', views.task_delete, name='task-delete'),
]
