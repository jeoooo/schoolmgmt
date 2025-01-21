from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from departments.models import Department

# Create your models here.
class Course(models.Model):
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True, blank=True)  # Example: "CS101"
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Course_detail", kwargs={"pk": self.pk})
