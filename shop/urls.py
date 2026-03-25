from django.urls import path
from .views import sklep, product_detail

urlpatterns = [
    path("", sklep, name="sklep"),
    path("<slug:slug>/", product_detail, name="product_detail"),
]