from rest_framework import serializers
from courses.models import Course

class CoursesSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 
            'department_id', 
            'department_name', 
            'name', 
            'code',
            # 'description', 
        ]
        read_only_fields = [
            'date_created', 
            'date_updated'
        ]

    def create(self, validated_data):
        department_id = validated_data.pop('department_id')
        course = Course.objects.create(department_id=department_id, **validated_data)
        return course

    def update(self, instance, validated_data):
        department_id = validated_data.pop('department_id', None)
        if department_id is not None:
            instance.department_id = department_id
        return super().update(instance, validated_data)