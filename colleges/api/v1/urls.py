from django.urls import path
from .views import CollegeListCreate, CollegeRetrieveUpdateDestroy

urlpatterns = [
    path('colleges/', CollegeListCreate.as_view(), name='college-list-create'),  # Combined endpoint for listing and creating colleges
    path('colleges/<int:pk>/', CollegeRetrieveUpdateDestroy.as_view(), name='college-update-delete'),
]