from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
import json

from users.models import User
from users.permissions import (
    IsAdmin, IsPrincipal, IsDean, IsTeacher, IsStudent, IsStaff,
    IsOwnerOrAdmin, IsCollegeManager, IsDepartmentManager
)
from colleges.models import College
from departments.models import Department

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        """Set up test data"""
        self.college = College.objects.create(
            name="Test College",
            address="123 Test St",
            contact_number="1234567890"
        )
        self.department = Department.objects.create(
            college=self.college,
            name="Computer Science",
            description="CS Department"
        )
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'student')  # default role
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(admin.username, 'admin')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)
    
    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(
            username='testuser',
            first_name='John',
            last_name='Doe',
            role='student'
        )
        expected = "John Doe (Student)"
        self.assertEqual(str(user), expected)
    
    def test_user_str_with_no_name(self):
        """Test user string representation when no first/last name"""
        user = User.objects.create_user(
            username='testuser',
            role='student'
        )
        expected = "testuser (Student)"
        self.assertEqual(str(user), expected)
    
    def test_get_full_name(self):
        """Test get_full_name method"""
        user = User.objects.create_user(
            username='testuser',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(user.get_full_name(), 'John Doe')
    
    def test_get_full_name_with_username_fallback(self):
        """Test get_full_name fallback to username"""
        user = User.objects.create_user(username='testuser')
        self.assertEqual(user.get_full_name(), 'testuser')
    
    def test_role_checking_methods(self):
        """Test role checking methods"""
        # Test admin
        admin = User.objects.create_user(username='admin', role='admin')
        self.assertTrue(admin.is_admin())
        self.assertFalse(admin.is_principal())
        self.assertFalse(admin.is_dean())
        self.assertFalse(admin.is_teacher())
        self.assertFalse(admin.is_student_user())
        self.assertFalse(admin.is_staff_user())
        self.assertTrue(admin.has_management_role())
        
        # Test student
        student = User.objects.create_user(username='student', role='student')
        self.assertFalse(student.is_admin())
        self.assertTrue(student.is_student_user())
        self.assertFalse(student.has_management_role())
        
        # Test teacher
        teacher = User.objects.create_user(username='teacher', role='teacher')
        self.assertTrue(teacher.is_teacher())
        self.assertFalse(teacher.has_management_role())
    
    def test_can_manage_college(self):
        """Test college management permissions"""
        # Admin can manage any college
        admin = User.objects.create_user(username='admin', role='admin')
        self.assertTrue(admin.can_manage_college(self.college))
        self.assertTrue(admin.can_manage_college())
        
        # Principal can manage their own college
        principal = User.objects.create_user(
            username='principal', 
            role='principal',
            college=self.college
        )
        self.assertTrue(principal.can_manage_college(self.college))
        
        other_college = College.objects.create(name="Other College")
        self.assertFalse(principal.can_manage_college(other_college))
        
        # Student cannot manage college
        student = User.objects.create_user(username='student', role='student')
        self.assertFalse(student.can_manage_college(self.college))
    
    def test_can_manage_department(self):
        """Test department management permissions"""
        # Admin can manage any department
        admin = User.objects.create_user(username='admin', role='admin')
        self.assertTrue(admin.can_manage_department(self.department))
        
        # Principal can manage departments in their college
        principal = User.objects.create_user(
            username='principal',
            role='principal', 
            college=self.college
        )
        self.assertTrue(principal.can_manage_department(self.department))
        
        # Dean can manage their own department
        dean = User.objects.create_user(
            username='dean',
            role='dean',
            department=self.department
        )
        self.assertTrue(dean.can_manage_department(self.department))
        
        other_department = Department.objects.create(
            college=self.college,
            name="Other Department"
        )
        self.assertFalse(dean.can_manage_department(other_department))
    
    def test_can_view_student(self):
        """Test student viewing permissions"""
        student = User.objects.create_user(
            username='student',
            role='student',
            department=self.department
        )
        
        # Admin can view any student
        admin = User.objects.create_user(username='admin', role='admin')
        self.assertTrue(admin.can_view_student(student))
        
        # Teacher can view students in their department
        teacher = User.objects.create_user(
            username='teacher',
            role='teacher',
            department=self.department
        )
        self.assertTrue(teacher.can_view_student(student))
        
        # Student can view themselves
        self.assertTrue(student.can_view_student(student))
        
        # Other students cannot view each other
        other_student = User.objects.create_user(
            username='otherstudent',
            role='student'
        )
        self.assertFalse(other_student.can_view_student(student))
    
    def test_unique_employee_id(self):
        """Test employee_id uniqueness"""
        User.objects.create_user(username='user1', employee_id='EMP001')
        
        with self.assertRaises(Exception):
            User.objects.create_user(username='user2', employee_id='EMP001')
    
    def test_unique_student_id(self):
        """Test student_id uniqueness"""
        User.objects.create_user(username='user1', student_id='STU001')
        
        with self.assertRaises(Exception):
            User.objects.create_user(username='user2', student_id='STU001')


class UserPermissionsTest(TestCase):
    """Test cases for User permissions"""
    
    def setUp(self):
        """Set up test data"""
        self.college = College.objects.create(name="Test College")
        self.department = Department.objects.create(
            college=self.college,
            name="Test Department"
        )
        
        self.admin = User.objects.create_user(
            username='admin',
            role='admin'
        )
        self.principal = User.objects.create_user(
            username='principal',
            role='principal',
            college=self.college
        )
        self.dean = User.objects.create_user(
            username='dean',
            role='dean',
            department=self.department
        )
        self.teacher = User.objects.create_user(
            username='teacher',
            role='teacher',
            department=self.department
        )
        self.student = User.objects.create_user(
            username='student',
            role='student'
        )
        self.staff = User.objects.create_user(
            username='staff',
            role='staff'
        )
    
    def test_is_admin_permission(self):
        """Test IsAdmin permission"""
        permission = IsAdmin()
        
        # Create mock request
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        self.assertTrue(permission.has_permission(MockRequest(self.admin), None))
        self.assertFalse(permission.has_permission(MockRequest(self.principal), None))
        self.assertFalse(permission.has_permission(MockRequest(self.student), None))
    
    def test_is_principal_permission(self):
        """Test IsPrincipal permission"""
        permission = IsPrincipal()
        
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        self.assertTrue(permission.has_permission(MockRequest(self.admin), None))
        self.assertTrue(permission.has_permission(MockRequest(self.principal), None))
        self.assertFalse(permission.has_permission(MockRequest(self.dean), None))
        self.assertFalse(permission.has_permission(MockRequest(self.student), None))
    
    def test_hierarchical_permissions(self):
        """Test hierarchical permission structure"""
        dean_permission = IsDean()
        teacher_permission = IsTeacher()
        student_permission = IsStudent()
        
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        # Admin should have all permissions
        admin_request = MockRequest(self.admin)
        self.assertTrue(dean_permission.has_permission(admin_request, None))
        self.assertTrue(teacher_permission.has_permission(admin_request, None))
        self.assertTrue(student_permission.has_permission(admin_request, None))
        
        # Teacher should have teacher and student permissions but not dean
        teacher_request = MockRequest(self.teacher)
        self.assertFalse(dean_permission.has_permission(teacher_request, None))
        self.assertTrue(teacher_permission.has_permission(teacher_request, None))
        self.assertTrue(student_permission.has_permission(teacher_request, None))


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.college = College.objects.create(name="Test College")
        self.department = Department.objects.create(
            college=self.college,
            name="Test Department"
        )
        
        # Create test users
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )
        
        self.student = User.objects.create_user(
            username='student',
            email='student@test.com',
            password='testpass123',
            role='student',
            first_name='John',
            last_name='Doe'
        )
        
        # URLs
        self.register_url = reverse('users_v1:register')
        self.login_url = reverse('users_v1:login')
        self.logout_url = reverse('users_v1:logout')
        self.profile_url = reverse('users_v1:profile')
        self.update_profile_url = reverse('users_v1:update_profile')
        self.change_password_url = reverse('users_v1:change_password')
    
    def get_tokens_for_user(self, user):
        """Helper method to get JWT tokens for user"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpass123!',
            'password_confirm': 'newpass123!',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Verify user was created
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@test.com')
        self.assertEqual(user.role, 'student')
    
    def test_user_registration_password_mismatch(self):
        """Test registration with password mismatch"""
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpass123!',
            'password_confirm': 'wrongpass',
            'role': 'student'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_user_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        data = {
            'username': 'admin',  # Already exists
            'email': 'newemail@test.com',
            'password': 'newpass123!',
            'password_confirm': 'newpass123!',
            'role': 'student'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_user_login_success(self):
        """Test successful user login"""
        data = {
            'username': 'student',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], 'student')
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'student',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_user_login_inactive_user(self):
        """Test login with inactive user"""
        # Deactivate user
        self.student.is_active = False
        self.student.save()
        
        data = {
            'username': 'student',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_logout_success(self):
        """Test successful user logout"""
        tokens = self.get_tokens_for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        data = {'refresh': tokens['refresh']}
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_user_profile(self):
        """Test getting user profile"""
        tokens = self.get_tokens_for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'student')
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
    
    def test_update_user_profile(self):
        """Test updating user profile"""
        tokens = self.get_tokens_for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '1234567890'
        }
        
        response = self.client.put(self.update_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify changes
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Updated')
        self.assertEqual(self.student.last_name, 'Name')
        self.assertEqual(self.student.phone, '1234567890')
    
    def test_change_password_success(self):
        """Test successful password change"""
        tokens = self.get_tokens_for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123!',
            'new_password_confirm': 'newpass123!'
        }
        
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify password was changed
        self.student.refresh_from_db()
        self.assertTrue(self.student.check_password('newpass123!'))
    
    def test_change_password_wrong_old_password(self):
        """Test password change with wrong old password"""
        tokens = self.get_tokens_for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpass123!',
            'new_password_confirm': 'newpass123!'
        }
        
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)
    
    def test_change_password_mismatch(self):
        """Test password change with new password mismatch"""
        tokens = self.get_tokens_for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123!',
            'new_password_confirm': 'differentpass!'
        }
        
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_unauthenticated_access(self):
        """Test accessing protected endpoints without authentication"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserViewSetTest(APITestCase):
    """Test cases for User ViewSet"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.college = College.objects.create(name="Test College")
        self.department = Department.objects.create(
            college=self.college,
            name="Test Department"
        )
        
        # Create users with different roles
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            role='admin'
        )
        
        self.principal = User.objects.create_user(
            username='principal',
            password='testpass123',
            role='principal',
            college=self.college
        )
        
        self.student = User.objects.create_user(
            username='student',
            password='testpass123',
            role='student',
            college=self.college
        )
        
        self.other_student = User.objects.create_user(
            username='otherstudent',
            password='testpass123',
            role='student'
        )
        
        self.users_url = reverse('users_v1:user-list')
    
    def get_tokens_for_user(self, user):
        """Helper method to get JWT tokens for user"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def test_admin_can_list_all_users(self):
        """Test that admin can list all users"""
        tokens = self.get_tokens_for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # All users
    
    def test_principal_can_list_college_users(self):
        """Test that principal can list users from their college"""
        tokens = self.get_tokens_for_user(self.principal)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Response might be paginated or direct list
        if 'results' in response.data:
            # Paginated response
            users_data = response.data['results']
        else:
            # Direct list response
            users_data = response.data
        
        # Should see principal and student from same college
        usernames = [user['username'] for user in users_data]
        self.assertIn('principal', usernames)
        self.assertIn('student', usernames)
        self.assertNotIn('otherstudent', usernames)
    
    def test_student_cannot_list_users(self):
        """Test that student cannot list users (requires principal permission)"""
        tokens = self.get_tokens_for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_create_user(self):
        """Test that admin can create users"""
        tokens = self.get_tokens_for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'testpass123',
            'role': 'teacher',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = self.client.post(self.users_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
    
    def test_non_admin_cannot_create_user(self):
        """Test that non-admin cannot create users"""
        tokens = self.get_tokens_for_user(self.principal)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'testpass123',
            'role': 'teacher'
        }
        
        response = self.client.post(self.users_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_user_activation_deactivation(self):
        """Test user activation and deactivation by admin"""
        tokens = self.get_tokens_for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        # Deactivate user
        deactivate_url = reverse('users_v1:user-deactivate', args=[self.student.id])
        response = self.client.post(deactivate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.student.refresh_from_db()
        self.assertFalse(self.student.is_active)
        
        # Activate user
        activate_url = reverse('users_v1:user-activate', args=[self.student.id])
        response = self.client.post(activate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.student.refresh_from_db()
        self.assertTrue(self.student.is_active)
    
    def test_users_by_role_filter(self):
        """Test filtering users by role"""
        tokens = self.get_tokens_for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        by_role_url = reverse('users_v1:user-by-role')
        response = self.client.get(by_role_url, {'role': 'student'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Response might be paginated or direct list
        if 'results' in response.data:
            # Paginated response
            users_data = response.data['results']
        else:
            # Direct list response
            users_data = response.data
        
        # Should only return students
        for user in users_data:
            self.assertEqual(user['role'], 'student')
    
    def test_user_retrieve_as_owner(self):
        """Test that user can retrieve their own data"""
        tokens = self.get_tokens_for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        user_detail_url = reverse('users_v1:user-detail', args=[self.student.id])
        response = self.client.get(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'student')
    
    def test_user_cannot_retrieve_other_users(self):
        """Test that user cannot retrieve other users' data"""
        tokens = self.get_tokens_for_user(self.student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        user_detail_url = reverse('users_v1:user-detail', args=[self.other_student.id])
        response = self.client.get(user_detail_url)
        # Expecting 404 because queryset filtering prevents access to other users
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserSerializerTest(TestCase):
    """Test cases for User serializers"""
    
    def setUp(self):
        """Set up test data"""
        self.college = College.objects.create(name="Test College")
        self.department = Department.objects.create(
            college=self.college,
            name="Test Department"
        )
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='student'
        )
    
    def test_user_profile_serializer(self):
        """Test UserProfileSerializer"""
        from users.api.v1.serializers import UserProfileSerializer
        
        serializer = UserProfileSerializer(self.user)
        data = serializer.data
        
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')
        self.assertEqual(data['role'], 'student')
        self.assertEqual(data['role_display'], 'Student')
    
    def test_user_registration_serializer_validation(self):
        """Test UserRegistrationSerializer validation"""
        from users.api.v1.serializers import UserRegistrationSerializer
        
        # Valid data
        valid_data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'testpass123!',
            'password_confirm': 'testpass123!',
            'role': 'student'
        }
        
        serializer = UserRegistrationSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        
        # Invalid data - password mismatch
        invalid_data = valid_data.copy()
        invalid_data['password_confirm'] = 'differentpass'
        
        serializer = UserRegistrationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
    
    def test_change_password_serializer(self):
        """Test ChangePasswordSerializer"""
        from users.api.v1.serializers import ChangePasswordSerializer
        
        # Mock request with user
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        # Valid data
        valid_data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123!',
            'new_password_confirm': 'newpass123!'
        }
        
        # Set a known password for the user
        self.user.set_password('testpass123')
        self.user.save()
        
        context = {'request': MockRequest(self.user)}
        serializer = ChangePasswordSerializer(data=valid_data, context=context)
        self.assertTrue(serializer.is_valid())
        
        # Invalid data - wrong old password
        invalid_data = valid_data.copy()
        invalid_data['old_password'] = 'wrongpass'
        
        serializer = ChangePasswordSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('old_password', serializer.errors)


class UserIntegrationTest(APITestCase):
    """Integration tests for User app workflow"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.college = College.objects.create(name="Integration College")
        self.department = Department.objects.create(
            college=self.college,
            name="Integration Department"
        )
        
        # Create admin user
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        
    def test_complete_user_lifecycle(self):
        """Test complete user lifecycle: register -> login -> update profile -> change password"""
        # 1. Register a new user
        register_url = reverse('users_v1:register')
        register_data = {
            'username': 'lifecycle_user',
            'email': 'lifecycle@test.com',
            'password': 'testpass123!',
            'password_confirm': 'testpass123!',
            'first_name': 'Lifecycle',
            'last_name': 'User',
            'role': 'student'
        }
        
        response = self.client.post(register_url, register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_id = response.data['user']['id']
        
        # 2. Login with the new user
        login_url = reverse('users_v1:login')
        login_data = {
            'username': 'lifecycle_user',
            'password': 'testpass123!'
        }
        
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']
        
        # 3. Update profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        update_url = reverse('users_v1:update_profile')
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '1234567890'
        }
        
        response = self.client.patch(update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'], 'Updated')
        
        # 4. Change password
        change_password_url = reverse('users_v1:change_password')
        password_data = {
            'old_password': 'testpass123!',
            'new_password': 'newpass456!',
            'new_password_confirm': 'newpass456!'
        }
        
        response = self.client.post(change_password_url, password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 5. Verify new password works
        new_login_data = {
            'username': 'lifecycle_user',
            'password': 'newpass456!'
        }
        
        response = self.client.post(login_url, new_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_admin_user_management_workflow(self):
        """Test admin managing users workflow"""
        # Login as admin
        admin_tokens = self.get_tokens_for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_tokens["access"]}')
        
        # Create a user via admin
        users_url = reverse('users_v1:user-list')
        user_data = {
            'username': 'managed_user',
            'email': 'managed@test.com',
            'password': 'managedpass123',
            'role': 'teacher',
            'first_name': 'Managed',
            'last_name': 'User',
            'college': self.college.id,
            'department': self.department.id
        }
        
        response = self.client.post(users_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user_id = response.data['id']
        
        # Deactivate the user
        deactivate_url = reverse('users_v1:user-deactivate', args=[created_user_id])
        response = self.client.post(deactivate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify user cannot login when deactivated
        login_url = reverse('users_v1:login')
        login_data = {
            'username': 'managed_user',
            'password': 'managedpass123'
        }
        
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Reactivate the user
        activate_url = reverse('users_v1:user-activate', args=[created_user_id])
        response = self.client.post(activate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify user can login again
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_role_based_access_control(self):
        """Test role-based access control across different scenarios"""
        # Create users with different roles
        principal = User.objects.create_user(
            username='principal_rbac',
            password='testpass123',
            role='principal',
            college=self.college
        )
        
        teacher = User.objects.create_user(
            username='teacher_rbac',
            password='testpass123',
            role='teacher',
            department=self.department
        )
        
        student = User.objects.create_user(
            username='student_rbac',
            password='testpass123',
            role='student',
            college=self.college
        )
        
        # Test principal can list college users
        principal_tokens = self.get_tokens_for_user(principal)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {principal_tokens["access"]}')
        
        users_url = reverse('users_v1:user-list')
        response = self.client.get(users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test teacher cannot list users (requires principal permission)
        teacher_tokens = self.get_tokens_for_user(teacher)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {teacher_tokens["access"]}')
        
        response = self.client.get(users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test student cannot list users
        student_tokens = self.get_tokens_for_user(student)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_tokens["access"]}')
        
        response = self.client.get(users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def get_tokens_for_user(self, user):
        """Helper method to get JWT tokens for user"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserEdgeCasesTest(TestCase):
    """Test edge cases and error conditions"""
    
    def setUp(self):
        """Set up test data"""
        self.college = College.objects.create(name="Edge Case College")
        self.department = Department.objects.create(
            college=self.college,
            name="Edge Case Department"
        )
    
    def test_user_with_special_characters_in_name(self):
        """Test user with special characters in name fields"""
        user = User.objects.create_user(
            username='special_user',
            first_name="José María",
            last_name="O'Connor-Smith",
            email='jose@test.com'
        )
        
        self.assertEqual(user.get_full_name(), "José María O'Connor-Smith")
        self.assertIn("José María O'Connor-Smith", str(user))
    
    def test_user_with_empty_names(self):
        """Test user behavior with empty name fields"""
        user = User.objects.create_user(
            username='empty_names',
            first_name='',
            last_name='',
            email='empty@test.com'
        )
        
        self.assertEqual(user.get_full_name(), 'empty_names')
        self.assertIn('empty_names', str(user))
    
    def test_user_with_only_whitespace_names(self):
        """Test user behavior with whitespace-only name fields"""
        user = User.objects.create_user(
            username='whitespace_names',
            first_name='   ',
            last_name='   ',
            email='whitespace@test.com'
        )
        
        self.assertEqual(user.get_full_name(), 'whitespace_names')
    
    def test_long_username_and_fields(self):
        """Test user with maximum length fields"""
        long_username = 'a' * 150  # Django's default max length for username
        user = User.objects.create_user(
            username=long_username,
            email='long@test.com'
        )
        
        self.assertEqual(len(user.username), 150)
        self.assertEqual(user.username, long_username)
    
    def test_user_role_methods_with_invalid_role(self):
        """Test role checking methods with edge cases"""
        # Create user with custom role (if somehow set)
        user = User.objects.create_user(username='invalid_role_user')
        user.role = 'invalid_role'
        user.save()
        
        # All role check methods should return False
        self.assertFalse(user.is_admin())
        self.assertFalse(user.is_principal())
        self.assertFalse(user.is_dean())
        self.assertFalse(user.is_teacher())
        self.assertFalse(user.is_student_user())
        self.assertFalse(user.is_staff_user())
        self.assertFalse(user.has_management_role())
    
    def test_user_permissions_with_none_values(self):
        """Test permission methods with None values"""
        user = User.objects.create_user(
            username='none_test_user',
            role='admin'
        )
        
        # Admin should handle None values gracefully
        self.assertTrue(user.can_manage_college(None))
        self.assertTrue(user.can_manage_department(None))
        self.assertTrue(user.can_view_student(None))
    
    def test_user_date_fields(self):
        """Test user date fields behavior"""
        from datetime import date, datetime
        
        birth_date = date(1990, 1, 1)
        user = User.objects.create_user(
            username='date_test_user',
            date_of_birth=birth_date
        )
        
        self.assertEqual(user.date_of_birth, birth_date)
        self.assertIsInstance(user.date_created, datetime)
        self.assertIsInstance(user.date_updated, datetime)
    
    def test_user_unique_constraints(self):
        """Test unique constraint violations"""
        # Create first user
        User.objects.create_user(
            username='unique_test1',
            employee_id='EMP001',
            student_id='STU001'
        )
        
        # Try to create user with same employee_id
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='unique_test2',
                employee_id='EMP001'
            )
        
        # Try to create user with same student_id
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='unique_test3',
                student_id='STU001'
            )
