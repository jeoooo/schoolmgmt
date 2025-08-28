from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'enrollment_date', 'grade']
    list_filter = ['status', 'enrollment_date', 'course__department']
    search_fields = [
        'student__first_name', 
        'student__last_name', 
        'student__student_id',
        'course__name',
        'course__code'
    ]
    raw_id_fields = ['student', 'course']
    readonly_fields = ['enrollment_date', 'last_updated']
    
    fieldsets = (
        (None, {
            'fields': ('student', 'course', 'status')
        }),
        ('Academic Info', {
            'fields': ('grade', 'notes')
        }),
        ('Timestamps', {
            'fields': ('enrollment_date', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'course', 'course__department')
