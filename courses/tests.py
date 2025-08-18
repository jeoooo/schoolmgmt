from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from colleges.models import College
from departments.models import Department
from courses.models import Course


class CourseModelTest(TestCase):
    """Test cases for Course model"""
    
    def setUp(self):
        self.college = College.objects.create(
            name="College of Engineering",
            address="123 Engineering St"
        )
        self.department = Department.objects.create(
            college=self.college,
            name="Computer Science Department"
        )
        self.course = Course.objects.create(
            department=self.department,
            name="Introduction to Programming",
            code="CS101",
            description="Basic programming concepts"
        )
    
    def test_course_creation(self):
        """Test course creation"""
        self.assertEqual(self.course.name, "Introduction to Programming")
        self.assertEqual(self.course.code, "CS101")
        self.assertEqual(self.course.department, self.department)
        self.assertEqual(self.course.description, "Basic programming concepts")
        self.assertIsNotNone(self.course.date_created)
        self.assertIsNotNone(self.course.date_updated)
    
    def test_course_str_representation(self):
        """Test course string representation"""
        self.assertEqual(str(self.course), "Introduction to Programming")
    
    def test_course_department_relationship(self):
        """Test course-department foreign key relationship"""
        self.assertEqual(self.course.department.name, "Computer Science Department")
    
    def test_course_unique_code(self):
        """Test that course code is unique"""
        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            Course.objects.create(
                department=self.department,
                name="Another Course",
                code="CS101"  # Duplicate code
            )
    
    def test_course_optional_fields(self):
        """Test that code and description are optional"""
        course = Course.objects.create(
            department=self.department,
            name="Basic Course"
        )
        self.assertEqual(course.code, "")
        self.assertIsNone(course.description)
    
    def test_course_cascade_delete(self):
        """Test that course is deleted when department is deleted"""
        course_id = self.course.id
        self.department.delete()
        
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(id=course_id)


class CourseAPITest(APITestCase):
    """Test cases for Course API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.college = College.objects.create(
            name="College of Science",
            address="Science Building"
        )
        self.department = Department.objects.create(
            college=self.college,
            name="Computer Science Department"
        )
        self.course_data = {
            'department_id': self.department.id,
            'name': 'Data Structures',
            'code': 'CS201',
            'description': 'Advanced data structures and algorithms'
        }
        self.course = Course.objects.create(
            department=self.department,
            name=self.course_data['name'],
            code=self.course_data['code'],
            description=self.course_data['description']
        )
    
    def test_get_course_list(self):
        """Test retrieving list of courses"""
        url = reverse('course-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Data Structures')
    
    def test_create_course(self):
        """Test creating a new course"""
        url = reverse('course-list-create')
        new_course_data = {
            'department_id': self.department.id,
            'name': 'Algorithms',
            'code': 'CS301',
            'description': 'Algorithm design and analysis'
        }
        response = self.client.post(url, new_course_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Algorithms')
    
    def test_get_course_detail(self):
        """Test retrieving a specific course"""
        url = reverse('course-update-delete', kwargs={'pk': self.course.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Data Structures')
    
    def test_update_course(self):
        """Test updating a course"""
        url = reverse('course-update-delete', kwargs={'pk': self.course.pk})
        updated_data = {
            'department_id': self.department.id,
            'name': 'Advanced Data Structures',
            'code': 'CS201',
            'description': 'Updated description'
        }
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, 'Advanced Data Structures')
    
    def test_delete_course(self):
        """Test deleting a course"""
        url = reverse('course-update-delete', kwargs={'pk': self.course.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)
    
    def test_create_course_invalid_department(self):
        """Test creating course with invalid department ID"""
        url = reverse('course-list-create')
        invalid_data = {
            'department_id': 999,  # Non-existent department
            'name': 'Invalid Course'
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_course_duplicate_code(self):
        """Test creating course with duplicate code"""
        url = reverse('course-list-create')
        duplicate_data = {
            'department_id': self.department.id,
            'name': 'Another Course',
            'code': 'CS201'  # Same as existing course
        }
        response = self.client.post(url, duplicate_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
