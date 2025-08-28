from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from enrollments.models import Enrollment
from students.models import Student
from courses.models import Course
from .serializers import (
    EnrollmentSerializer, 
    EnrollmentCreateSerializer,
    StudentEnrollmentSerializer,
    CourseEnrollmentSerializer
)

class EnrollmentListCreate(generics.ListCreateAPIView):
    """List all enrollments and create new enrollment"""
    queryset = Enrollment.objects.all().select_related('student', 'course', 'course__department')
    serializer_class = EnrollmentSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EnrollmentCreateSerializer
        return EnrollmentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by student if provided
        student_id = self.request.query_params.get('student', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Filter by course if provided
        course_id = self.request.query_params.get('course', None)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        # Filter by status if provided
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset

class EnrollmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete enrollment by ID"""
    queryset = Enrollment.objects.all().select_related('student', 'course', 'course__department')
    serializer_class = EnrollmentSerializer

@api_view(['GET'])
def student_enrollments(request, student_id):
    """Get all enrollments for a specific student"""
    student = get_object_or_404(Student, id=student_id)
    enrollments = Enrollment.objects.filter(student=student).select_related('course', 'course__department')
    
    # Filter by status if provided
    status = request.query_params.get('status', None)
    if status:
        enrollments = enrollments.filter(status=status)
    
    serializer = StudentEnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def course_enrollments(request, course_id):
    """Get all enrollments for a specific course"""
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    
    # Filter by status if provided
    status = request.query_params.get('status', None)
    if status:
        enrollments = enrollments.filter(status=status)
    
    serializer = CourseEnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def enroll_student(request):
    """Enroll a student in a course"""
    serializer = EnrollmentCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            enrollment = serializer.save()
            response_serializer = EnrollmentSerializer(enrollment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def drop_enrollment(request, enrollment_id):
    """Drop an enrollment (change status to dropped)"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    enrollment.drop()
    serializer = EnrollmentSerializer(enrollment)
    return Response(serializer.data)

@api_view(['POST'])
def complete_enrollment(request, enrollment_id):
    """Complete an enrollment (change status to completed)"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    grade = request.data.get('grade', None)
    enrollment.complete(grade=grade)
    serializer = EnrollmentSerializer(enrollment)
    return Response(serializer.data)

@api_view(['GET'])
def enrollment_stats(request):
    """Get enrollment statistics"""
    total_enrollments = Enrollment.objects.count()
    active_enrollments = Enrollment.objects.filter(status='enrolled').count()
    completed_enrollments = Enrollment.objects.filter(status='completed').count()
    dropped_enrollments = Enrollment.objects.filter(status='dropped').count()
    
    return Response({
        'total_enrollments': total_enrollments,
        'active_enrollments': active_enrollments,
        'completed_enrollments': completed_enrollments,
        'dropped_enrollments': dropped_enrollments,
    })
