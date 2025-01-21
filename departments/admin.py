from django.contrib import admin
from departments.models import Department

# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'college', 'name', 'description', 'date_created', 'date_updated')
    list_filter = ('college',)
    
admin.site.register(Department, DepartmentAdmin)