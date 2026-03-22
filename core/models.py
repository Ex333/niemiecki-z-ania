from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class HomePage(models.Model):

    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)

    offer_title = models.CharField(max_length=200, blank=True)
    target_title = models.CharField(max_length=200, blank=True)

    about_title = models.CharField(max_length=200, blank=True)
    about_text = models.TextField(blank=True)

    cta_title = models.CharField(max_length=200, blank=True)
    cta_button = models.CharField(max_length=200, blank=True)

    cta2_title = models.CharField(max_length=200, blank=True)
    cta2_text = models.TextField(blank=True)
    cta2_button = models.CharField(max_length=200, blank=True)

    content = CKEditor5Field(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Strona główna"