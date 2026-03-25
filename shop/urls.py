from django.urls import path
from shop.views import  sklep, product_detail


urlpatterns = [
    path("", sklep, name="sklep"),
    path("<slug:slug>/", product_detail, name="sklep_detail"),
]

