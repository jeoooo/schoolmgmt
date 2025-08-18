from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from colleges.models import College
from departments.models import Department


class DepartmentModelTest(TestCase):
    """Test cases for Department model"""
    
    def setUp(self):
        self.college = College.objects.create(
            name="College of Engineering",
            address="123 Engineering St"
        )
        self.department = Department.objects.create(
            college=self.college,
            name="Computer Science Department",
            description="Department of Computer Science and Engineering"
        )
    
    def test_department_creation(self):
        """Test department creation"""
        self.assertEqual(self.department.name, "Computer Science Department")
        self.assertEqual(self.department.college, self.college)
        self.assertEqual(self.department.description, "Department of Computer Science and Engineering")
        self.assertIsNotNone(self.department.date_created)
        self.assertIsNotNone(self.department.date_updated)
    
    def test_department_str_representation(self):
        """Test department string representation"""
        self.assertEqual(str(self.department), "Computer Science Department")
    
    def test_department_college_relationship(self):
        """Test department-college foreign key relationship"""
        self.assertEqual(self.department.college.name, "College of Engineering")
    
    def test_department_optional_description(self):
        """Test that description is optional"""
        dept = Department.objects.create(
            college=self.college,
            name="Mathematics Department"
        )
        self.assertIsNone(dept.description)
    
    def test_department_cascade_delete(self):
        """Test that department is deleted when college is deleted"""
        dept_id = self.department.id
        self.college.delete()
        
        with self.assertRaises(Department.DoesNotExist):
            Department.objects.get(id=dept_id)


class DepartmentAPITest(APITestCase):
    """Test cases for Department API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.college = College.objects.create(
            name="College of Science",
            address="Science Building"
        )
        self.department_data = {
            'college_id': self.college.id,
            'name': 'Physics Department',
            'description': 'Department of Physics'
        }
        self.department = Department.objects.create(
            college=self.college,
            name=self.department_data['name'],
            description=self.department_data['description']
        )
    
    def test_get_department_list(self):
        """Test retrieving list of departments"""
        url = reverse('department-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Physics Department')
    
    def test_create_department(self):
        """Test creating a new department"""
        url = reverse('department-list-create')
        new_department_data = {
            'college_id': self.college.id,
            'name': 'Chemistry Department',
            'description': 'Department of Chemistry'
        }
        response = self.client.post(url, new_department_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Chemistry Department')
    
    def test_get_department_detail(self):
        """Test retrieving a specific department"""
        url = reverse('department-update-delete', kwargs={'pk': self.department.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Physics Department')
    
    def test_update_department(self):
        """Test updating a department"""
        url = reverse('department-update-delete', kwargs={'pk': self.department.pk})
        updated_data = {
            'college_id': self.college.id,
            'name': 'Updated Physics Department',
            'description': 'Updated description'
        }
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.name, 'Updated Physics Department')
    
    def test_delete_department(self):
        """Test deleting a department"""
        url = reverse('department-update-delete', kwargs={'pk': self.department.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.count(), 0)
    
    def test_create_department_invalid_college(self):
        """Test creating department with invalid college ID"""
        url = reverse('department-list-create')
        invalid_data = {
            'college_id': 999,  # Non-existent college
            'name': 'Invalid Department'
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
