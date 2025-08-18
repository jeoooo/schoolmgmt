from rest_framework import serializers
from professors.models import Professor

class ProfessorsSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    
    
    class Meta:
        model = Professor
        fields = [
            'id', 
            'department_id', 
            'department_name', 
            'first_name', 
            'last_name',
            'specialization',
            'contact_number',
        ]
    
    def create(self, validated_data):
            from departments.models import Department
            department_id = validated_data.pop('department_id')
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                raise serializers.ValidationError({'department_id': 'Invalid department ID.'})
            professor = Professor.objects.create(department=department, **validated_data)
            return professor
    
    def update(self, instance, validated_data):
        department_id = validated_data.pop('department_id', None)
        if department_id is not None:
            instance.department_id = department_id
        return super().update(instance, validated_data)