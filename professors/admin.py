from django.contrib import admin
from professors.models import Professor

# Register your models here.
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'first_name', 'last_name', 'specialization', 'contact_number', 'date_created', 'date_updated')
    list_filter = ('department',)
    
admin.site.register(Professor, ProfessorAdmin)