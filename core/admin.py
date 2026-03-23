from django.contrib import admin
from .models import HomePage, Material, Category


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("title",)}