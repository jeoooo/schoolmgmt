from django.contrib import admin
from colleges.models import College

# Register your models here.
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'contact_number', 'date_created', 'date_updated')
    list_filter = ('date_created', 'date_updated')

admin.site.register(College, CollegeAdmin)