from rest_framework import serializers
from subjects.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Subject
        fields = [
            'id',
            'course_id',
            'course_name',
            'name',
            'code',
            'description',
        ]

    def create(self, validated_data):
        from courses.models import Course
        course_id = validated_data.pop('course_id')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError({'course_id': 'Invalid course ID.'})
        subject = Subject.objects.create(course=course, **validated_data)
        return subject

    def update(self, instance, validated_data):
        course_id = validated_data.pop('course_id', None)
        if course_id is not None:
            from courses.models import Course
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                raise serializers.ValidationError({'course_id': 'Invalid course ID.'})
            instance.course = course
        return super().update(instance, validated_data)