from rest_framework import serializers
from subjects.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subject
        fields = [
            'id', 
            'department_id', 
            'department_name', 
            'name', 
            'description', 
        ]
        read_only_fields = [
            'date_created', 
            'date_updated'
        ]

    def create(self, validated_data):
        department_id = validated_data.pop('department_id')
        subject = Subject.objects.create(department_id=department_id, **validated_data)
        return subject

    def update(self, instance, validated_data):
        department_id = validated_data.pop('department_id', None)
        if department_id is not None:
            instance.department_id = department_id
        return super().update(instance, validated_data)