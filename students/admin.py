from django.contrib import admin
from students.models import Student

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'student_id', 'email', 'contact_number', 'department')
    list_filter = ('department',)

admin.site.register(Student, StudentAdmin)