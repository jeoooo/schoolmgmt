from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Permission class to check if user is system administrator
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.is_admin()
        )

class IsPrincipal(BasePermission):
    """
    Permission class to check if user is principal
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['admin', 'principal']
        )

class IsDean(BasePermission):
    """
    Permission class to check if user is dean
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['admin', 'principal', 'dean']
        )

class IsTeacher(BasePermission):
    """
    Permission class to check if user is teacher
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['admin', 'principal', 'dean', 'teacher']
        )

class IsStudent(BasePermission):
    """
    Permission class to check if user is student
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['admin', 'principal', 'dean', 'teacher', 'student']
        )

class IsStaff(BasePermission):
    """
    Permission class to check if user is staff
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['admin', 'principal', 'dean', 'staff']
        )

class IsOwnerOrAdmin(BasePermission):
    """
    Permission class to check if user is owner of object or admin
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions for any authenticated user
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions only to owner or admin
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_admin()
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user or request.user.is_admin()
        else:
            return request.user.is_admin()

class IsCollegeManager(BasePermission):
    """
    Permission class to check if user can manage college
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'college'):
            return request.user.can_manage_college(obj.college)
        elif obj.__class__.__name__ == 'College':
            return request.user.can_manage_college(obj)
        return request.user.is_admin()

class IsDepartmentManager(BasePermission):
    """
    Permission class to check if user can manage department
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'department'):
            return request.user.can_manage_department(obj.department)
        elif obj.__class__.__name__ == 'Department':
            return request.user.can_manage_department(obj)
        return request.user.is_admin()

class CanViewStudent(BasePermission):
    """
    Permission class to check if user can view student
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj.__class__.__name__ == 'Student':
            return request.user.can_view_student(obj)
        return request.user.has_management_role()

class ReadOnlyOrAdmin(BasePermission):
    """
    Permission class for read-only access or admin write access
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_admin()
