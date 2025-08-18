from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.
class College(models.Model):
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.name or not self.name.strip():
            raise ValidationError({'name': 'Name cannot be empty or whitespace.'})
    name = models.CharField(max_length=255, blank=False, null=False)
    address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = _("College")
        verbose_name_plural = _("Colleges")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("College_detail", kwargs={"pk": self.pk})
