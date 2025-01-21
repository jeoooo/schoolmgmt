from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from colleges.models import College

# Create your models here.
class Department(models.Model):
    college = models.ForeignKey("colleges.College", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Department_detail", kwargs={"pk": self.pk})
