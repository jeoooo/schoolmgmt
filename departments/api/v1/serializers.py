from rest_framework import serializers
from departments.models import Department
        
class DepartmentsSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)
    college_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Department
        fields = [
            'id', 
            'college_id', 
            'college_name', 
            'name', 
            # 'description', 
        ]
        read_only_fields = [
            'date_created', 
            'date_updated'
        ]

    def create(self, validated_data):
            from colleges.models import College
            college_id = validated_data.pop('college_id')
            try:
                college = College.objects.get(id=college_id)
            except College.DoesNotExist:
                raise serializers.ValidationError({'college_id': 'Invalid college ID.'})
            department = Department.objects.create(college=college, **validated_data)
            return department

    def update(self, instance, validated_data):
        college_id = validated_data.pop('college_id', None)
        if college_id is not None:
            instance.college_id = college_id
        return super().update(instance, validated_data)