from django.urls import path
from .views import DepartmentListCreate, DepartmentRetrieveUpdateDestroy

urlpatterns = [
    path('departments/', DepartmentListCreate.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroy.as_view(), name='department-update-delete'),
]
