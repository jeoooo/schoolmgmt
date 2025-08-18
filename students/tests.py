from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from colleges.models import College
from departments.models import Department
from students.models import Student


class StudentModelTest(TestCase):
    """Test cases for Student model"""
    
    def setUp(self):
        self.college = College.objects.create(
            name="College of Engineering",
            address="123 Engineering St"
        )
        self.department = Department.objects.create(
            college=self.college,
            name="Computer Science Department"
        )
        self.student = Student.objects.create(
            department=self.department,
            first_name="John",
            last_name="Doe",
            student_id="2024001",
            email="john.doe@university.edu",
            contact_number="123-456-7890"
        )
    
    def test_student_creation(self):
        """Test student creation"""
        self.assertEqual(self.student.first_name, "John")
        self.assertEqual(self.student.last_name, "Doe")
        self.assertEqual(self.student.student_id, "2024001")
        self.assertEqual(self.student.email, "john.doe@university.edu")
        self.assertEqual(self.student.contact_number, "123-456-7890")
        self.assertEqual(self.student.department, self.department)
    
    def test_student_str_representation(self):
        """Test student string representation"""
        self.assertEqual(str(self.student), "John Doe")
    
    def test_student_department_relationship(self):
        """Test student-department foreign key relationship"""
        self.assertEqual(self.student.department.name, "Computer Science Department")
    
    def test_student_unique_student_id(self):
        """Test that student ID is unique"""
        with self.assertRaises(Exception):  # IntegrityError
            Student.objects.create(
                department=self.department,
                first_name="Jane",
                last_name="Smith",
                student_id="2024001",  # Duplicate student ID
                email="jane.smith@university.edu",
                contact_number="098-765-4321"
            )
    
    def test_student_cascade_delete(self):
        """Test that student is deleted when department is deleted"""
        student_id = self.student.id
        self.department.delete()
        
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(id=student_id)


class StudentAPITest(APITestCase):
    """Test cases for Student API endpoints"""
    
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
        self.student_data = {
            'department_id': self.department.id,
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'student_id': '2024002',
            'email': 'alice.johnson@university.edu',
            'contact_number': '555-123-4567'
        }
        self.student = Student.objects.create(
            department=self.department,
            first_name=self.student_data['first_name'],
            last_name=self.student_data['last_name'],
            student_id=self.student_data['student_id'],
            email=self.student_data['email'],
            contact_number=self.student_data['contact_number']
        )
    
    def test_get_student_list(self):
        """Test retrieving list of students"""
        url = reverse('student-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Alice')
    
    def test_create_student(self):
        """Test creating a new student"""
        url = reverse('student-list-create')
        new_student_data = {
            'department_id': self.department.id,
            'first_name': 'Bob',
            'last_name': 'Wilson',
            'student_id': '2024003',
            'email': 'bob.wilson@university.edu',
            'contact_number': '555-987-6543'
        }
        response = self.client.post(url, new_student_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(response.data['first_name'], 'Bob')
    
    def test_get_student_detail(self):
        """Test retrieving a specific student"""
        url = reverse('student-update-delete', kwargs={'pk': self.student.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Alice')
    
    def test_update_student(self):
        """Test updating a student"""
        url = reverse('student-update-delete', kwargs={'pk': self.student.pk})
        updated_data = {
            'department_id': self.department.id,
            'first_name': 'Alice',
            'last_name': 'Johnson-Smith',
            'student_id': '2024002',
            'email': 'alice.johnsonsmith@university.edu',
            'contact_number': '555-123-4567'
        }
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.last_name, 'Johnson-Smith')
    
    def test_delete_student(self):
        """Test deleting a student"""
        url = reverse('student-update-delete', kwargs={'pk': self.student.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)
    
    def test_create_student_invalid_email(self):
        """Test creating student with invalid email"""
        url = reverse('student-list-create')
        invalid_data = {
            'department_id': self.department.id,
            'first_name': 'Invalid',
            'last_name': 'Student',
            'student_id': '2024004',
            'email': 'invalid-email',  # Invalid email format
            'contact_number': '555-123-4567'
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_student_duplicate_student_id(self):
        """Test creating student with duplicate student ID"""
        url = reverse('student-list-create')
        duplicate_data = {
            'department_id': self.department.id,
            'first_name': 'Duplicate',
            'last_name': 'Student',
            'student_id': '2024002',  # Same as existing student
            'email': 'duplicate@university.edu',
            'contact_number': '555-123-4567'
        }
        response = self.client.post(url, duplicate_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
