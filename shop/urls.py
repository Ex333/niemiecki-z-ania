from django.urls import path
from shop.views import  sklep


urlpatterns = [
    path("", sklep, name="sklep"),
]

