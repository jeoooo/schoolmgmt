from rest_framework import serializers
from departments.models import Department
from colleges.api.v1.serializers import CollegeSerializer
        
class DepartmentSerializer(serializers.ModelSerializer):
    college = CollegeSerializer(read_only=True)
    college_name = serializers.CharField(source='college.name', read_only=True)
    college_id = serializers.IntegerField(source='college.id', read_only=True)
    
    class Meta:
        model = Department
        fields = [
            'id', 
            'college', 
            'college_id', 
            'college_name', 
            'name', 
            # 'description', 
        ]
        read_only_fields = [
            'date_created', 
            'date_updated'
        ]