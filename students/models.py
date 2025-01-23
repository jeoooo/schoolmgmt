from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from departments.models import Department

# Create your models here.
class Student(models.Model):
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='students')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=15, unique=True)  # Student ID Number
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Student_detail", kwargs={"pk": self.pk})
