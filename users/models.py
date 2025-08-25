from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model with role-based access control
    """
    ROLE_CHOICES = [
        ('admin', 'System Administrator'),
        ('principal', 'Principal'),
        ('dean', 'Dean'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('staff', 'Staff'),
    ]
    
    # Additional fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    college = models.ForeignKey(
        'colleges.College', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='users'
    )
    department = models.ForeignKey(
        'departments.Department', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='users'
    )
    employee_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    student_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        permissions = [
            ("can_manage_all_colleges", "Can manage all colleges"),
            ("can_manage_own_college", "Can manage own college"),
            ("can_manage_all_departments", "Can manage all departments"),
            ("can_manage_own_department", "Can manage own department"),
            ("can_view_all_students", "Can view all students"),
            ("can_manage_own_students", "Can manage own students"),
            ("can_view_reports", "Can view reports"),
            ("can_manage_system_settings", "Can manage system settings"),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def get_full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def is_admin(self):
        """Check if user is system admin"""
        return self.role == 'admin'

    def is_principal(self):
        """Check if user is principal"""
        return self.role == 'principal'

    def is_dean(self):
        """Check if user is dean"""
        return self.role == 'dean'

    def is_teacher(self):
        """Check if user is teacher"""
        return self.role == 'teacher'

    def is_student_user(self):
        """Check if user is student"""
        return self.role == 'student'

    def is_staff_user(self):
        """Check if user is staff"""
        return self.role == 'staff'

    def has_management_role(self):
        """Check if user has management role (admin, principal, dean)"""
        return self.role in ['admin', 'principal', 'dean']

    def can_manage_college(self, college=None):
        """Check if user can manage a specific college or any college"""
        if self.is_admin():
            return True
        if self.is_principal() and college and self.college == college:
            return True
        return False

    def can_manage_department(self, department=None):
        """Check if user can manage a specific department or any department"""
        if self.is_admin():
            return True
        if self.is_principal() and department and self.college == department.college:
            return True
        if self.is_dean() and department and self.department == department:
            return True
        return False

    def can_view_student(self, student=None):
        """Check if user can view a specific student"""
        if self.has_management_role():
            return True
        if self.is_teacher() and student and self.department == student.department:
            return True
        if self.is_student_user() and student and self == student:
            return True
        return False
