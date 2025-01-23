from django.urls import path
from .views import SubjectListCreate, SubjectRetrieveUpdateDestroy

urlpatterns = [
    path('subjects/', SubjectListCreate.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroy.as_view(), name='subject-update-delete'),
]
