from django.urls import path
from .views import ProfessorListCreate, ProfessorRetrieveUpdateDestroy

urlpatterns = [
    path('professors/', ProfessorListCreate.as_view(), name='professor-list-create'),
    path('professors/<int:pk>/', ProfessorRetrieveUpdateDestroy.as_view(), name='professor-update-delete'),
]
