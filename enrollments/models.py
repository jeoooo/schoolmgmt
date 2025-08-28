from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ValidationError
from students.models import Student
from courses.models import Course

class Enrollment(models.Model):
    ENROLLMENT_STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS_CHOICES, default='enrolled')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    grade = models.CharField(max_length=5, blank=True, null=True)  # e.g., 'A', 'B+', 'C', etc.
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollments")
        unique_together = ['student', 'course']  # Prevent duplicate enrollments
        ordering = ['-enrollment_date']
    
    def clean(self):
        # Custom validation
        if self.student and self.course:
            # Check if student is already enrolled in this course
            if Enrollment.objects.filter(
                student=self.student, 
                course=self.course,
                status='enrolled'
            ).exclude(pk=self.pk).exists():
                raise ValidationError('Student is already enrolled in this course.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course} ({self.status})"
    
    def get_absolute_url(self):
        return reverse("enrollment_detail", kwargs={"pk": self.pk})

    @property
    def is_active(self):
        return self.status == 'enrolled'
    
    def drop(self):
        """Helper method to drop the enrollment"""
        self.status = 'dropped'
        self.save()
    
    def complete(self, grade=None):
        """Helper method to complete the enrollment with optional grade"""
        self.status = 'completed'
        if grade:
            self.grade = grade
        self.save()
