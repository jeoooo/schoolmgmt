from rest_framework import serializers
from students.models import Student

class StudentsSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    
    
    class Meta:
        model = Student
        fields = [
            'id',
            'department_id',
            'department_name',
            'first_name',
            'last_name',
            'student_id',
            'email',
            'contact_number',
        ]

    def create(self, validated_data):
        from departments.models import Department
        department_id = validated_data.pop('department_id')
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise serializers.ValidationError({'department_id': 'Invalid department ID.'})
        student = Student.objects.create(department=department, **validated_data)
        return student

    def update(self, instance, validated_data):
        department_id = validated_data.pop('department_id', None)
        if department_id is not None:
            from departments.models import Department
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                raise serializers.ValidationError({'department_id': 'Invalid department ID.'})
            instance.department = department
        return super().update(instance, validated_data)