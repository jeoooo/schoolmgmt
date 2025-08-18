from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from departments.models import Department
# Create your models here.
class Professor(models.Model):
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='professors')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    # subjects = models.ManyToManyField(Subject, related_name='professors')  # Professors teach multiple subjects

    class Meta:
        verbose_name = _("Professor")
        verbose_name_plural = _("Professors")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("Professor_detail", kwargs={"pk": self.pk})
