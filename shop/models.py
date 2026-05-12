from django.db import models
from django.utils import timezone

from datetime import timedelta
import uuid


# =========== SHOP MODELS ==========

class ShopCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        ShopCategory,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(
        max_length=255,
        unique=True
    )

    slug = models.SlugField(unique=True)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    file = models.FileField(
        upload_to='products/',
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='products/images/',
        null=True,
        blank=True
    )

    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# =========== ORDER ==========

class Order(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    email = models.EmailField()

    paypal_order_id = models.CharField(
        max_length=255,
        unique=True
    )

    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.email} - {self.product.name}"


# =========== DOWNLOAD TOKEN ==========

class DownloadToken(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="download_token"
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Token for {self.order.email}"