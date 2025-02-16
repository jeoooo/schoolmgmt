from django.contrib import admin
from departments.models import Department

# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'name', 'code', 'description')
    list_filter = ('course',)
    
admin.site.register(Department, DepartmentAdmin)