from rest_framework import serializers
from courses.models import Course

class CoursesSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_id = serializers.IntegerField(write_only=True, source='department')

    class Meta:
        model = Course
        fields = [
            'id', 
            'department_id', 
            'department_name', 
            'name', 
            'code',
            'description', 
            'date_created', 
            'date_updated'
        ]
        read_only_fields = [
            'date_created', 
            'date_updated'
        ]

    def create(self, validated_data):
        from departments.models import Department
        department_id = validated_data.pop('department')
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise serializers.ValidationError({'department': 'Invalid department ID.'})
        course = Course.objects.create(department=department, **validated_data)
        return course

    def update(self, instance, validated_data):
        department_id = validated_data.pop('department', None)
        if department_id is not None:
            from departments.models import Department
            try:
                department = Department.objects.get(id=department_id)
                instance.department = department
            except Department.DoesNotExist:
                raise serializers.ValidationError({'department': 'Invalid department ID.'})
        return super().update(instance, validated_data)