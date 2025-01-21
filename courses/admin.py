from django.contrib import admin
from courses.models import Course

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'name', 'code', 'description', 'date_created', 'date_updated')
    list_filter = ('department',)
    
admin.site.register(Course, CourseAdmin)