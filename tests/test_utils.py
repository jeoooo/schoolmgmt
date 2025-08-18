"""
Test configuration and utilities for the school management system
"""

from django.test import TestCase
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class BaseTestCase(TestCase):
    """Base test case with common setup for all model tests"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up data for the whole TestCase"""
        # This method is called once for the entire test case
        pass
    
    def setUp(self):
        """Set up data for each test method"""
        # This method is called before each test
        pass


class BaseAPITestCase(APITestCase):
    """Base API test case with authentication setup"""
    
    def setUp(self):
        """Set up user and authentication for API tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Uncomment the following line if you want to test with authentication
        # self.client.force_authenticate(user=self.user)


class TestDataMixin:
    """Mixin providing common test data creation methods"""
    
    def create_test_college(self, name="Test College", **kwargs):
        """Create a test college with default or custom data"""
        from colleges.models import College
        defaults = {
            'name': name,
            'address': '123 Test Street',
            'contact_number': '555-0100'
        }
        defaults.update(kwargs)
        return College.objects.create(**defaults)
    
    def create_test_department(self, college=None, name="Test Department", **kwargs):
        """Create a test department with default or custom data"""
        from departments.models import Department
        if college is None:
            college = self.create_test_college()
        
        defaults = {
            'college': college,
            'name': name,
            'description': 'Test department description'
        }
        defaults.update(kwargs)
        return Department.objects.create(**defaults)
    
    def create_test_course(self, department=None, name="Test Course", **kwargs):
        """Create a test course with default or custom data"""
        from courses.models import Course
        if department is None:
            department = self.create_test_department()
        
        defaults = {
            'department': department,
            'name': name,
            'code': 'TC001',
            'description': 'Test course description'
        }
        defaults.update(kwargs)
        return Course.objects.create(**defaults)
    
    def create_test_subject(self, course=None, name="Test Subject", **kwargs):
        """Create a test subject with default or custom data"""
        from subjects.models import Subject
        if course is None:
            course = self.create_test_course()
        
        defaults = {
            'course': course,
            'name': name,
            'code': 'TS001',
            'description': 'Test subject description'
        }
        defaults.update(kwargs)
        return Subject.objects.create(**defaults)
    
    def create_test_student(self, department=None, student_id="ST001", **kwargs):
        """Create a test student with default or custom data"""
        from students.models import Student
        if department is None:
            department = self.create_test_department()
        
        defaults = {
            'department': department,
            'first_name': 'Test',
            'last_name': 'Student',
            'student_id': student_id,
            'email': f'test.student.{student_id.lower()}@university.edu',
            'contact_number': '555-0101'
        }
        defaults.update(kwargs)
        return Student.objects.create(**defaults)
    
    def create_test_professor(self, department=None, **kwargs):
        """Create a test professor with default or custom data"""
        from professors.models import Professor
        if department is None:
            department = self.create_test_department()
        
        defaults = {
            'department': department,
            'first_name': 'Dr. Test',
            'last_name': 'Professor',
            'specialization': 'Test Specialization',
            'contact_number': '555-0102'
        }
        defaults.update(kwargs)
        return Professor.objects.create(**defaults)


# Test settings
TEST_SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    'PASSWORD_HASHERS': [
        'django.contrib.auth.hashers.MD5PasswordHasher',  # Faster for tests
    ],
    'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
}
