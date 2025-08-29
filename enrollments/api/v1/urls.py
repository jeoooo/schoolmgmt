from django.urls import path
from .views import (
    EnrollmentListCreate,
    EnrollmentRetrieveUpdateDestroy,
    student_enrollments,
    course_enrollments,
    enroll_student,
    drop_enrollment,
    complete_enrollment,
    enrollment_stats,
)

urlpatterns = [
    # Basic CRUD operations
    path('enrollments/', EnrollmentListCreate.as_view(), name='enrollment-list-create'),
    path('enrollments/<int:pk>/', EnrollmentRetrieveUpdateDestroy.as_view(), name='enrollment-detail'),
    
    # Student-specific enrollments
    path('students/<int:student_id>/enrollments/', student_enrollments, name='student-enrollments'),
    
    # Course-specific enrollments
    path('courses/<int:course_id>/enrollments/', course_enrollments, name='course-enrollments'),
    
    # Enrollment actions
    path('enroll/', enroll_student, name='enroll-student'),
    path('enrollments/<int:enrollment_id>/drop/', drop_enrollment, name='drop-enrollment'),
    path('enrollments/<int:enrollment_id>/complete/', complete_enrollment, name='complete-enrollment'),
    
    # Statistics
    path('enrollments/stats/', enrollment_stats, name='enrollment-stats'),
]
