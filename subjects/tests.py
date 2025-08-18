from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from colleges.models import College
from departments.models import Department
from courses.models import Course
from subjects.models import Subject


class SubjectModelTest(TestCase):
    """Test cases for Subject model"""
    
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
            name="Computer Science",
            code="CS",
            description="Computer Science Course"
        )
        self.subject = Subject.objects.create(
            course=self.course,
            name="Programming Fundamentals",
            code="CS101",
            description="Introduction to programming concepts"
        )
    
    def test_subject_creation(self):
        """Test subject creation"""
        self.assertEqual(self.subject.name, "Programming Fundamentals")
        self.assertEqual(self.subject.code, "CS101")
        self.assertEqual(self.subject.description, "Introduction to programming concepts")
        self.assertEqual(self.subject.course, self.course)
    
    def test_subject_str_representation(self):
        """Test subject string representation"""
        self.assertEqual(str(self.subject), "Programming Fundamentals")
    
    def test_subject_course_relationship(self):
        """Test subject-course foreign key relationship"""
        self.assertEqual(self.subject.course.name, "Computer Science")
    
    def test_subject_unique_code(self):
        """Test that subject code is unique"""
        with self.assertRaises(Exception):  # IntegrityError
            Subject.objects.create(
                course=self.course,
                name="Another Subject",
                code="CS101",  # Duplicate code
                description="Another description"
            )
    
    def test_subject_cascade_delete(self):
        """Test that subject is deleted when course is deleted"""
        subject_id = self.subject.id
        self.course.delete()
        
        with self.assertRaises(Subject.DoesNotExist):
            Subject.objects.get(id=subject_id)


class SubjectAPITest(APITestCase):
    """Test cases for Subject API endpoints"""
    
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
        self.course = Course.objects.create(
            department=self.department,
            name="Computer Science",
            code="CS"
        )
        self.subject_data = {
            'course_id': self.course.id,
            'name': 'Data Structures',
            'code': 'CS201',
            'description': 'Advanced data structures and algorithms'
        }
        self.subject = Subject.objects.create(
            course=self.course,
            name=self.subject_data['name'],
            code=self.subject_data['code'],
            description=self.subject_data['description']
        )
    
    def test_get_subject_list(self):
        """Test retrieving list of subjects"""
        url = reverse('subject-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Data Structures')
    
    def test_create_subject(self):
        """Test creating a new subject"""
        url = reverse('subject-list-create')
        new_subject_data = {
            'course_id': self.course.id,
            'name': 'Algorithms',
            'code': 'CS301',
            'description': 'Algorithm design and analysis'
        }
        response = self.client.post(url, new_subject_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subject.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Algorithms')
    
    def test_get_subject_detail(self):
        """Test retrieving a specific subject"""
        url = reverse('subject-update-delete', kwargs={'pk': self.subject.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Data Structures')
    
    def test_update_subject(self):
        """Test updating a subject"""
        url = reverse('subject-update-delete', kwargs={'pk': self.subject.pk})
        updated_data = {
            'course_id': self.course.id,
            'name': 'Advanced Data Structures',
            'code': 'CS201',
            'description': 'Updated description'
        }
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.name, 'Advanced Data Structures')
    
    def test_delete_subject(self):
        """Test deleting a subject"""
        url = reverse('subject-update-delete', kwargs={'pk': self.subject.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subject.objects.count(), 0)
    
    def test_create_subject_invalid_course(self):
        """Test creating subject with invalid course ID"""
        url = reverse('subject-list-create')
        invalid_data = {
            'course_id': 999,  # Non-existent course
            'name': 'Invalid Subject',
            'code': 'INV001',
            'description': 'Invalid subject'
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_subject_duplicate_code(self):
        """Test creating subject with duplicate code"""
        url = reverse('subject-list-create')
        duplicate_data = {
            'course_id': self.course.id,
            'name': 'Another Subject',
            'code': 'CS201',  # Same as existing subject
            'description': 'Another description'
        }
        response = self.client.post(url, duplicate_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
