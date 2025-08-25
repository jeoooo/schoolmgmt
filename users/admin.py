from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form for admin
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'email', 'first_name', 'last_name', 'role', 'phone',
            'college', 'department', 'employee_id', 'student_id',
            'date_of_birth', 'address'
        )

class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form for admin
    """
    class Meta:
        model = User
        fields = '__all__'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin
    """
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'role', 'college', 'department', 'is_active', 'date_joined'
    ]
    list_filter = [
        'role', 'is_active', 'is_staff', 'is_superuser', 
        'college', 'department', 'date_joined'
    ]
    search_fields = [
        'username', 'email', 'first_name', 'last_name', 
        'employee_id', 'student_id'
    ]
    ordering = ['username']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'role', 'phone', 'college', 'department',
                'employee_id', 'student_id', 'date_of_birth', 'address'
            )
        }),
        ('Timestamps', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': (
                'email', 'first_name', 'last_name', 'role', 'phone',
                'college', 'department', 'employee_id', 'student_id',
                'date_of_birth', 'address'
            )
        }),
    )
    
    readonly_fields = ['date_created', 'date_updated']
    
    def get_queryset(self, request):
        """
        Filter queryset based on user role
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'role'):
            if request.user.is_admin():
                return qs
            elif request.user.is_principal():
                return qs.filter(college=request.user.college)
            elif request.user.is_dean():
                return qs.filter(department=request.user.department)
        return qs.filter(id=request.user.id)
    
    def has_change_permission(self, request, obj=None):
        """
        Check if user has permission to change user objects
        """
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if hasattr(request.user, 'role'):
            if request.user.is_admin():
                return True
            elif request.user.is_principal() and obj.college == request.user.college:
                return True
            elif obj == request.user:
                return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        """
        Check if user has permission to delete user objects
        """
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if hasattr(request.user, 'role'):
            return request.user.is_admin()
        return False
