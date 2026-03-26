from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator


def sklep(request):
    products = Product.objects.filter(available=True).order_by("name")

    paginator = Paginator(products, 9)  
    page_number = request.GET.get("page")  
    page_obj = paginator.get_page(page_number)

    return render(request, "shop/sklep.html", {
        "page_obj": page_obj
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, "shop/product_detail.html", {  
        "product": product
    })