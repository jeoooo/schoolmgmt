from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from students.models import Student
from courses.models import Course
from departments.models import Department
from colleges.models import College
from .models import Enrollment

User = get_user_model()

class EnrollmentModelTest(TestCase):
    """Test cases for the Enrollment model"""
    
    def setUp(self):
        """Set up test data"""
        # Create a college
        self.college = College.objects.create(
            name="Test College",
            address="123 Test St"
        )
        
        # Create a department
        self.department = Department.objects.create(
            name="Computer Science",
            college=self.college
        )
        
        # Create a course
        self.course = Course.objects.create(
            name="Introduction to Python",
            code="CS101",
            description="Learn Python programming",
            department=self.department
        )
        
        # Create a student
        self.student = Student.objects.create(
            first_name="John",
            last_name="Doe",
            student_id="STU001",
            email="john.doe@example.com",
            contact_number="1234567890",
            department=self.department
        )
    
    def test_enrollment_creation(self):
        """Test creating a valid enrollment"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            status='enrolled'
        )
        
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.course, self.course)
        self.assertEqual(enrollment.status, 'enrolled')
        self.assertTrue(enrollment.is_active)
        self.assertIsNotNone(enrollment.enrollment_date)
    
    def test_enrollment_string_representation(self):
        """Test the string representation of enrollment"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        
        expected_str = f"{self.student} enrolled in {self.course} (enrolled)"
        self.assertEqual(str(enrollment), expected_str)
    
    def test_duplicate_enrollment_prevention(self):
        """Test that duplicate active enrollments are prevented"""
        # Create first enrollment
        Enrollment.objects.create(
            student=self.student,
            course=self.course,
            status='enrolled'
        )
        
        # Try to create duplicate enrollment
        duplicate_enrollment = Enrollment(
            student=self.student,
            course=self.course,
            status='enrolled'
        )
        
        with self.assertRaises(ValidationError):
            duplicate_enrollment.clean()
    
    def test_enrollment_drop_method(self):
        """Test the drop method"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        
        enrollment.drop()
        self.assertEqual(enrollment.status, 'dropped')
        self.assertFalse(enrollment.is_active)
    
    def test_enrollment_complete_method(self):
        """Test the complete method"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        
        enrollment.complete(grade='A')
        self.assertEqual(enrollment.status, 'completed')
        self.assertEqual(enrollment.grade, 'A')
        self.assertFalse(enrollment.is_active)
    
    def test_enrollment_unique_together_constraint(self):
        """Test the unique_together constraint works properly"""
        # Create first enrollment
        Enrollment.objects.create(
            student=self.student,
            course=self.course,
            status='enrolled'
        )
        
        # Try to create another enrollment (should fail at database level)
        with self.assertRaises(Exception):  # IntegrityError in real database
            Enrollment.objects.create(
                student=self.student,
                course=self.course,
                status='enrolled'
            )


class EnrollmentAPITest(APITestCase):
    """Test cases for the Enrollment API endpoints"""
    
    def setUp(self):
        """Set up test data and authentication"""
        # Create a user for authentication
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role="admin"
        )
        
        # Create test data
        self.college = College.objects.create(
            name="Test College",
            address="123 Test St"
        )
        
        self.department = Department.objects.create(
            name="Computer Science",
            college=self.college
        )
        
        self.course1 = Course.objects.create(
            name="Introduction to Python",
            code="CS101",
            description="Learn Python programming",
            department=self.department
        )
        
        self.course2 = Course.objects.create(
            name="Data Structures",
            code="CS102",
            description="Learn data structures",
            department=self.department
        )
        
        self.student = Student.objects.create(
            first_name="John",
            last_name="Doe",
            student_id="STU001",
            email="john.doe@example.com",
            contact_number="1234567890",
            department=self.department
        )
        
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
    
    def test_create_enrollment(self):
        """Test creating an enrollment via API"""
        url = reverse('enrollment-list-create')
        data = {
            'student': self.student.id,
            'course': self.course1.id,
            'notes': 'Test enrollment'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)
        
        enrollment = Enrollment.objects.first()
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.course, self.course1)
    
    def test_list_enrollments(self):
        """Test listing enrollments via API"""
        # Create test enrollments
        Enrollment.objects.create(
            student=self.student,
            course=self.course1
        )
        Enrollment.objects.create(
            student=self.student,
            course=self.course2
        )
        
        url = reverse('enrollment-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response is paginated or not
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 2)
        else:
            self.assertEqual(len(response.data), 2)
    
    def test_filter_enrollments_by_student(self):
        """Test filtering enrollments by student"""
        # Create another student
        student2 = Student.objects.create(
            first_name="Jane",
            last_name="Smith",
            student_id="STU002",
            email="jane.smith@example.com",
            contact_number="0987654321",
            department=self.department
        )
        
        # Create enrollments for both students
        Enrollment.objects.create(student=self.student, course=self.course1)
        Enrollment.objects.create(student=student2, course=self.course1)
        
        url = reverse('enrollment-list-create')
        response = self.client.get(url, {'student': self.student.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle paginated response
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['student'], self.student.id)
    
    def test_filter_enrollments_by_course(self):
        """Test filtering enrollments by course"""
        # Create enrollments for different courses
        Enrollment.objects.create(student=self.student, course=self.course1)
        Enrollment.objects.create(student=self.student, course=self.course2)
        
        url = reverse('enrollment-list-create')
        response = self.client.get(url, {'course': self.course1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle paginated response
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['course'], self.course1.id)
    
    def test_filter_enrollments_by_status(self):
        """Test filtering enrollments by status"""
        enrollment1 = Enrollment.objects.create(student=self.student, course=self.course1)
        enrollment2 = Enrollment.objects.create(student=self.student, course=self.course2)
        enrollment2.drop()  # Change status to dropped
        
        url = reverse('enrollment-list-create')
        response = self.client.get(url, {'status': 'enrolled'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle paginated response
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['status'], 'enrolled')
    
    def test_get_enrollment_detail(self):
        """Test getting enrollment details"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course1
        )
        
        url = reverse('enrollment-detail', kwargs={'pk': enrollment.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], enrollment.id)
        self.assertEqual(response.data['student'], self.student.id)
        self.assertEqual(response.data['course'], self.course1.id)
    
    def test_update_enrollment(self):
        """Test updating an enrollment"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course1
        )
        
        url = reverse('enrollment-detail', kwargs={'pk': enrollment.id})
        data = {
            'student': self.student.id,
            'course': self.course1.id,
            'status': 'completed',
            'grade': 'A'
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.status, 'completed')
        self.assertEqual(enrollment.grade, 'A')
    
    def test_delete_enrollment(self):
        """Test deleting an enrollment"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course1
        )
        
        url = reverse('enrollment-detail', kwargs={'pk': enrollment.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Enrollment.objects.count(), 0)
    
    def test_student_enrollments_endpoint(self):
        """Test the student-specific enrollments endpoint"""
        Enrollment.objects.create(student=self.student, course=self.course1)
        Enrollment.objects.create(student=self.student, course=self.course2)
        
        url = reverse('student-enrollments', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_course_enrollments_endpoint(self):
        """Test the course-specific enrollments endpoint"""
        # Create another student
        student2 = Student.objects.create(
            first_name="Jane",
            last_name="Smith",
            student_id="STU002",
            email="jane.smith@example.com",
            contact_number="0987654321",
            department=self.department
        )
        
        Enrollment.objects.create(student=self.student, course=self.course1)
        Enrollment.objects.create(student=student2, course=self.course1)
        
        url = reverse('course-enrollments', kwargs={'course_id': self.course1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_enroll_student_endpoint(self):
        """Test the enroll student endpoint"""
        url = reverse('enroll-student')
        data = {
            'student': self.student.id,
            'course': self.course1.id,
            'notes': 'Quick enrollment'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)
    
    def test_drop_enrollment_endpoint(self):
        """Test the drop enrollment endpoint"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course1
        )
        
        url = reverse('drop-enrollment', kwargs={'enrollment_id': enrollment.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.status, 'dropped')
    
    def test_complete_enrollment_endpoint(self):
        """Test the complete enrollment endpoint"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course1
        )
        
        url = reverse('complete-enrollment', kwargs={'enrollment_id': enrollment.id})
        data = {'grade': 'B+'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.status, 'completed')
        self.assertEqual(enrollment.grade, 'B+')
    
    def test_enrollment_stats_endpoint(self):
        """Test the enrollment statistics endpoint"""
        # Create enrollments with different statuses
        enrollment1 = Enrollment.objects.create(student=self.student, course=self.course1)
        enrollment2 = Enrollment.objects.create(student=self.student, course=self.course2)
        enrollment2.drop()
        
        url = reverse('enrollment-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_enrollments'], 2)
        self.assertEqual(response.data['active_enrollments'], 1)
        self.assertEqual(response.data['dropped_enrollments'], 1)
        self.assertEqual(response.data['completed_enrollments'], 0)
    
    def test_prevent_duplicate_enrollment(self):
        """Test that duplicate enrollments are prevented via API"""
        # Create first enrollment
        Enrollment.objects.create(
            student=self.student,
            course=self.course1,
            status='enrolled'
        )
        
        # Try to create duplicate
        url = reverse('enroll-student')
        data = {
            'student': self.student.id,
            'course': self.course1.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated requests are denied"""
        self.client.force_authenticate(user=None)
        
        url = reverse('enrollment-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_enrollment_workflow(self):
        """Test the complete enrollment workflow"""
        # 1. Enroll student in course
        enroll_url = reverse('enroll-student')
        enroll_data = {
            'student': self.student.id,
            'course': self.course1.id,
            'notes': 'Workflow test enrollment'
        }
        
        response = self.client.post(enroll_url, enroll_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        enrollment_id = response.data['id']
        
        # 2. Verify enrollment exists
        enrollment = Enrollment.objects.get(id=enrollment_id)
        self.assertEqual(enrollment.status, 'enrolled')
        
        # 3. Update grade
        update_url = reverse('enrollment-detail', kwargs={'pk': enrollment_id})
        update_data = {
            'student': self.student.id,
            'course': self.course1.id,
            'status': 'enrolled',
            'grade': 'A-'
        }
        
        response = self.client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Complete the enrollment
        complete_url = reverse('complete-enrollment', kwargs={'enrollment_id': enrollment_id})
        complete_data = {'grade': 'A'}
        
        response = self.client.post(complete_url, complete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 5. Verify final state
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.status, 'completed')
        self.assertEqual(enrollment.grade, 'A')

    def test_enrollment_serializer_validation(self):
        """Test enrollment serializer validation"""
        from enrollments.api.v1.serializers import EnrollmentSerializer
        
        # Test valid data
        valid_data = {
            'student': self.student.id,
            'course': self.course1.id,
            'status': 'enrolled'
        }
        
        serializer = EnrollmentSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        
        # Test duplicate enrollment prevention
        Enrollment.objects.create(
            student=self.student,
            course=self.course1,
            status='enrolled'
        )
        
        duplicate_serializer = EnrollmentSerializer(data=valid_data)
        self.assertFalse(duplicate_serializer.is_valid())
        # The error comes from database unique constraint, not our custom validation
        self.assertIn('unique', str(duplicate_serializer.errors).lower())
