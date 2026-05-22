from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from django.core.paginator import Paginator
from urllib.parse import urlencode

from .models import (
    Product,
    Order
)


# =========================
# SHOP
# =========================

def sklep(request):

    products = Product.objects.filter(
        available=True
    ).order_by("name")

    paginator = Paginator(
        products,
        9
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        "shop/sklep.html",
        {
            "page_obj": page_obj
        }
    )


# =========================
# PRODUCT DETAIL
# =========================

def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        available=True
    )

    return render(
        request,
        "shop/product_detail.html",
        {
            "product": product
        }
    )


# =========================
# CREATE ORDER
# =========================

def create_order(request, slug):

    if request.method != "POST":

        return redirect(
            "product_detail",
            slug=slug
        )

    product = get_object_or_404(
        Product,
        slug=slug,
        available=True
    )

    customer_name = request.POST.get(
        "customer_name"
    )

    email = request.POST.get(
        "email"
    )

    if not customer_name or not email:

        return render(
            request,
            "shop/product_detail.html",
            {
                "product": product,
                "error": "Uzupełnij wszystkie pola."
            }
        )

    Order.objects.create(
        product=product,
        customer_name=customer_name,
        email=email
    )

    # URL po sukcesie i anulowaniu
    success_url = request.build_absolute_uri(
        "/shop/payment-success/"
    )

    cancel_url = request.build_absolute_uri(
        "/shop/payment-cancel/"
    )

    # PAYPAL REDIRECT
    paypal_params = urlencode({
        "business": "annawac1987@gmail.com",
        "item_name": product.name,
        "amount": f"{product.price:.2f}",
        "currency_code": "PLN",

        "return": success_url,
        "cancel_return": cancel_url,
        "rm": "2",
    })

    paypal_url = (
        "https://www.paypal.com/cgi-bin/webscr"
        f"?cmd=_xclick&{paypal_params}"
    )

    return redirect(
        paypal_url
    )


# =========================
# PAYMENT PAGES
# =========================

def payment_success(request):

    return render(
        request,
        "shop/payment_success.html"
    )


def payment_cancel(request):

    return render(
        request,
        "shop/payment_cancel.html"
    )