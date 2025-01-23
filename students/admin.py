from django.contrib import admin
from students.models import Student

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department', 'roll_number', 'date_created', 'date_updated')
    list_filter = ('department',)    

admin.site.register(Student, StudentAdmin)    