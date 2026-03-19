from django.shortcuts import render
from .models import Product

def sklep(request):
    products = Product.objects.all()
    return render(request, "sklep.html", {"products": products})