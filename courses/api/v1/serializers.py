from rest_framework import serializers
from courses.models import Course
from departments.api.v1.serializers import DepartmentSerializer

class CoursesSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_id = serializers.IntegerField(source='department.id', read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 
            'department', 
            'department_id', 
            'department_name', 
            'name', 
            # 'description', 
        ]
        read_only_fields = [
            'date_created', 
            'date_updated'
        ]