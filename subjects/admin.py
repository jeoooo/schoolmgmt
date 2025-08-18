from django.contrib import admin
from subjects.models import Subject

# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'name', 'code', 'description')
    list_filter = ('course',)
    
admin.site.register(Subject, SubjectAdmin)