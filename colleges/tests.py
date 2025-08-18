from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from colleges.models import College


class CollegeModelTest(TestCase):
    """Test cases for College model"""
    
    def setUp(self):
        self.college = College.objects.create(
            name="College of Computer Science",
            address="123 University Ave",
            contact_number="123-456-7890"
        )
    
    def test_college_creation(self):
        """Test college creation"""
        self.assertEqual(self.college.name, "College of Computer Science")
        self.assertEqual(self.college.address, "123 University Ave")
        self.assertEqual(self.college.contact_number, "123-456-7890")
        self.assertIsNotNone(self.college.date_created)
        self.assertIsNotNone(self.college.date_updated)
    
    def test_college_str_representation(self):
        """Test college string representation"""
        self.assertEqual(str(self.college), "College of Computer Science")
    
    def test_college_fields_optional(self):
        """Test that address and contact_number are optional"""
        college = College.objects.create(name="College of Arts")
        self.assertIsNone(college.address)
        self.assertIsNone(college.contact_number)
    
    def test_college_update(self):
        """Test college update functionality"""
        original_updated = self.college.date_updated
        self.college.name = "Updated College Name"
        self.college.save()
        self.college.refresh_from_db()
        
        self.assertEqual(self.college.name, "Updated College Name")
        self.assertGreater(self.college.date_updated, original_updated)


class CollegeAPITest(APITestCase):
    """Test cases for College API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.college_data = {
            'name': 'College of Engineering',
            'address': '456 Tech Street',
            'contact_number': '098-765-4321'
        }
        self.college = College.objects.create(**self.college_data)
    
    def test_get_college_list(self):
        """Test retrieving list of colleges"""
        url = reverse('college-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'College of Engineering')
    
    def test_create_college(self):
        """Test creating a new college"""
        url = reverse('college-list-create')
        new_college_data = {
            'name': 'College of Business',
            'address': '789 Business Blvd',
            'contact_number': '555-123-4567'
        }
        response = self.client.post(url, new_college_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(College.objects.count(), 2)
        self.assertEqual(response.data['name'], 'College of Business')
    
    def test_get_college_detail(self):
        """Test retrieving a specific college"""
        url = reverse('college-update-delete', kwargs={'pk': self.college.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'College of Engineering')
    
    def test_update_college(self):
        """Test updating a college"""
        url = reverse('college-update-delete', kwargs={'pk': self.college.pk})
        updated_data = {
            'name': 'Updated College Name',
            'address': 'Updated Address',
            'contact_number': '111-222-3333'
        }
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.college.refresh_from_db()
        self.assertEqual(self.college.name, 'Updated College Name')
    
    def test_delete_college(self):
        """Test deleting a college"""
        url = reverse('college-update-delete', kwargs={'pk': self.college.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(College.objects.count(), 0)
    
    def test_create_college_missing_name(self):
        """Test creating college without required name field"""
        url = reverse('college-list-create')
        invalid_data = {
            'address': '789 Business Blvd',
            'contact_number': '555-123-4567'
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
