from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from courses.models import Course
# Create your models here.
class Subject(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)  # Example: "CS101"
    description = models.TextField()
    

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Subject_detail", kwargs={"pk": self.pk})
