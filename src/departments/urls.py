from django.urls import path
from . import views

urlpatterns = [
    path('', views.DepartmentListView.as_view(), name='department-list'),
    path('add/', views.DepartmentCreateView.as_view(), name='department-add'),
    path('<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    path('<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department-update'),
    path('<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department-delete'),
]
