from rest_framework import serializers
from enrollments.models import Enrollment
from students.models import Student
from courses.models import Course

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student.last_name', read_only=True)
    student_id_number = serializers.CharField(source='student.student_id', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    department_name = serializers.CharField(source='course.department.name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id',
            'student',
            'course',
            'student_name',
            'student_last_name',
            'student_id_number',
            'course_name',
            'course_code',
            'department_name',
            'status',
            'enrollment_date',
            'last_updated',
            'grade',
            'notes',
        ]
        read_only_fields = ['enrollment_date', 'last_updated']

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')
        
        if student and course:
            # Check for existing active enrollment
            existing_enrollment = Enrollment.objects.filter(
                student=student,
                course=course,
                status='enrolled'
            )
            
            # If this is an update, exclude the current instance
            if self.instance:
                existing_enrollment = existing_enrollment.exclude(pk=self.instance.pk)
            
            if existing_enrollment.exists():
                raise serializers.ValidationError(
                    "Student is already enrolled in this course."
                )
        
        return data

class EnrollmentCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating enrollments"""
    
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'notes']

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for showing enrollments from student perspective"""
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_description = serializers.CharField(source='course.description', read_only=True)
    department_name = serializers.CharField(source='course.department.name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id',
            'course',
            'course_name',
            'course_code',
            'course_description',
            'department_name',
            'status',
            'enrollment_date',
            'grade',
        ]
        read_only_fields = ['enrollment_date']

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for showing enrollments from course perspective"""
    student_name = serializers.CharField(source='student.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student.last_name', read_only=True)
    student_id_number = serializers.CharField(source='student.student_id', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id',
            'student',
            'student_name',
            'student_last_name',
            'student_id_number',
            'student_email',
            'status',
            'enrollment_date',
            'grade',
            'notes',
        ]
        read_only_fields = ['enrollment_date']
