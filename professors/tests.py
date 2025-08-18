from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from colleges.models import College
from departments.models import Department
from professors.models import Professor


class ProfessorModelTest(TestCase):
    """Test cases for Professor model"""
    
    def setUp(self):
        self.college = College.objects.create(
            name="College of Engineering",
            address="123 Engineering St"
        )
        self.department = Department.objects.create(
            college=self.college,
            name="Computer Science Department"
        )
        self.professor = Professor.objects.create(
            department=self.department,
            first_name="Dr. Jane",
            last_name="Smith",
            specialization="Machine Learning",
            contact_number="123-456-7890"
        )
    
    def test_professor_creation(self):
        """Test professor creation"""
        self.assertEqual(self.professor.first_name, "Dr. Jane")
        self.assertEqual(self.professor.last_name, "Smith")
        self.assertEqual(self.professor.specialization, "Machine Learning")
        self.assertEqual(self.professor.contact_number, "123-456-7890")
        self.assertEqual(self.professor.department, self.department)
    
    def test_professor_str_representation(self):
        """Test professor string representation"""
        self.assertEqual(str(self.professor), "Dr. Jane Smith")
    
    def test_professor_department_relationship(self):
        """Test professor-department foreign key relationship"""
        self.assertEqual(self.professor.department.name, "Computer Science Department")
    
    def test_professor_cascade_delete(self):
        """Test that professor is deleted when department is deleted"""
        professor_id = self.professor.id
        self.department.delete()
        
        with self.assertRaises(Professor.DoesNotExist):
            Professor.objects.get(id=professor_id)


class ProfessorAPITest(APITestCase):
    """Test cases for Professor API endpoints"""
    
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
        self.professor_data = {
            'department_id': self.department.id,
            'first_name': 'Dr. Robert',
            'last_name': 'Johnson',
            'specialization': 'Data Science',
            'contact_number': '555-123-4567'
        }
        self.professor = Professor.objects.create(
            department=self.department,
            first_name=self.professor_data['first_name'],
            last_name=self.professor_data['last_name'],
            specialization=self.professor_data['specialization'],
            contact_number=self.professor_data['contact_number']
        )
    
    def test_get_professor_list(self):
        """Test retrieving list of professors"""
        url = reverse('professor-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Dr. Robert')
    
    def test_create_professor(self):
        """Test creating a new professor"""
        url = reverse('professor-list-create')
        new_professor_data = {
            'department_id': self.department.id,
            'first_name': 'Dr. Sarah',
            'last_name': 'Wilson',
            'specialization': 'Artificial Intelligence',
            'contact_number': '555-987-6543'
        }
        response = self.client.post(url, new_professor_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professor.objects.count(), 2)
        self.assertEqual(response.data['first_name'], 'Dr. Sarah')
    
    def test_get_professor_detail(self):
        """Test retrieving a specific professor"""
        url = reverse('professor-update-delete', kwargs={'pk': self.professor.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Dr. Robert')
    
    def test_update_professor(self):
        """Test updating a professor"""
        url = reverse('professor-update-delete', kwargs={'pk': self.professor.pk})
        updated_data = {
            'department_id': self.department.id,
            'first_name': 'Dr. Robert',
            'last_name': 'Johnson',
            'specialization': 'Advanced Data Science',
            'contact_number': '555-123-4567'
        }
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.professor.refresh_from_db()
        self.assertEqual(self.professor.specialization, 'Advanced Data Science')
    
    def test_delete_professor(self):
        """Test deleting a professor"""
        url = reverse('professor-update-delete', kwargs={'pk': self.professor.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Professor.objects.count(), 0)
    
    def test_create_professor_invalid_department(self):
        """Test creating professor with invalid department ID"""
        url = reverse('professor-list-create')
        invalid_data = {
            'department_id': 999,  # Non-existent department
            'first_name': 'Dr. Invalid',
            'last_name': 'Professor',
            'specialization': 'Unknown',
            'contact_number': '555-123-4567'
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
