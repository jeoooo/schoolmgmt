from django.urls import path
from .views import CourseListCreate, CourseRetrieveUpdateDestroy

urlpatterns = [
    path('courses/', CourseListCreate.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroy.as_view(), name='course-update-delete'),
]
