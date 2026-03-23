from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import FileExtensionValidator

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


# ******************* MATERIAŁY *****************************
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Material(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pdf = models.FileField(
    upload_to="materials/",
    validators=[FileExtensionValidator(allowed_extensions=["pdf", "docx", "xlsx"])]
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        def __str__(self):
            return selff.title
        



