import json

import requests

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Product, Order


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
            "product": product,
            "paypal_client_id": settings.PAYPAL_CLIENT_ID,
        }
    )


# =========================
# PAYPAL ACCESS TOKEN
# =========================

def get_paypal_access_token():

    response = requests.post(
        f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token",
        auth=(
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_SECRET
        ),
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },
        data={
            "grant_type": "client_credentials"
        },
        timeout=15,
    )

    response.raise_for_status()

    return response.json()["access_token"]


# =========================
# CREATE PAYPAL ORDER
# =========================

@require_POST
def create_order(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        available=True
    )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "Nieprawidłowe dane."
            },
            status=400
        )

    customer_name = str(
        data.get("customer_name", "")
    ).strip()

    email = str(
        data.get("email", "")
    ).strip()

    if not customer_name or not email:

        return JsonResponse(
            {
                "error": "Podaj imię oraz adres email."
            },
            status=400
        )

    # =========================
    # GET PAYPAL TOKEN
    # =========================

    try:
        access_token = get_paypal_access_token()

    except requests.RequestException as e:

        print(
            "PayPal token error:",
            e
        )

        return JsonResponse(
            {
                "error": "Nie udało się połączyć z PayPal."
            },
            status=502
        )

    # =========================
    # CREATE LOCAL ORDER
    # =========================

    order = Order.objects.create(
        product=product,
        customer_name=customer_name,
        email=email,
        paid=False,
    )

    # =========================
    # CREATE PAYPAL ORDER
    # =========================

    paypal_data = {
        "intent": "CAPTURE",

        "purchase_units": [
            {
                "reference_id": str(order.id),

                "description": product.name,

                "custom_id": str(order.id),

                "amount": {
                    "currency_code": "PLN",
                    "value": f"{product.price:.2f}",
                },
            }
        ],
    }

    try:

        response = requests.post(
            f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            json=paypal_data,
            timeout=15,
        )

        response.raise_for_status()

        paypal_order = response.json()

    except requests.RequestException as e:

        print(
            "PayPal create order error:",
            e
        )

        order.delete()

        return JsonResponse(
            {
                "error": "Nie udało się utworzyć płatności PayPal."
            },
            status=502
        )

    paypal_order_id = paypal_order.get("id")

    if not paypal_order_id:

        order.delete()

        return JsonResponse(
            {
                "error": "PayPal nie zwrócił identyfikatora zamówienia."
            },
            status=502
        )

    # =========================
    # SAVE PAYPAL ORDER ID
    # =========================

    order.paypal_order_id = paypal_order_id

    order.save(
        update_fields=[
            "paypal_order_id"
        ]
    )

    return JsonResponse(
        {
            "id": paypal_order_id
        }
    )


# =========================
# CAPTURE PAYPAL ORDER
# =========================

@require_POST
def capture_order(request):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "Nieprawidłowe dane."
            },
            status=400
        )

    paypal_order_id = str(
        data.get("orderID", "")
    ).strip()

    if not paypal_order_id:

        return JsonResponse(
            {
                "error": "Brak identyfikatora zamówienia PayPal."
            },
            status=400
        )

    # =========================
    # FIND LOCAL ORDER
    # =========================

    order = get_object_or_404(
        Order,
        paypal_order_id=paypal_order_id
    )

    # =========================
    # ALREADY PAID?
    # =========================

    if order.paid:

        return JsonResponse(
            {
                "success": True,
                "redirect_url": "/sklep/payment-success/"
            }
        )

    # =========================
    # GET PAYPAL TOKEN
    # =========================

    try:
        access_token = get_paypal_access_token()

    except requests.RequestException as e:

        print(
            "PayPal token error:",
            e
        )

        return JsonResponse(
            {
                "error": "Nie udało się połączyć z PayPal."
            },
            status=502
        )

    # =========================
    # CAPTURE
    # =========================

    try:

        response = requests.post(
            (
                f"{settings.PAYPAL_BASE_URL}"
                f"/v2/checkout/orders/"
                f"{paypal_order_id}/capture"
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            json={},
            timeout=15,
        )

        response.raise_for_status()

        capture_data = response.json()

    except requests.RequestException as e:

        print(
            "PayPal capture error:",
            e
        )

        return JsonResponse(
            {
                "error": "Nie udało się potwierdzić płatności PayPal."
            },
            status=502
        )

    # =========================
    # VERIFY PAYMENT
    # =========================

    if capture_data.get("status") != "COMPLETED":

        return JsonResponse(
            {
                "error": "Płatność nie została potwierdzona."
            },
            status=400
        )

    purchase_units = capture_data.get(
        "purchase_units",
        []
    )

    if not purchase_units:

        return JsonResponse(
            {
                "error": "PayPal nie zwrócił informacji o płatności."
            },
            status=400
        )

    payments = purchase_units[0].get(
        "payments",
        {}
    )

    captures = payments.get(
        "captures",
        []
    )

    if not captures:

        return JsonResponse(
            {
                "error": "Nie znaleziono potwierdzonej transakcji."
            },
            status=400
        )

    capture = captures[0]

    if capture.get("status") != "COMPLETED":

        return JsonResponse(
            {
                "error": "Transakcja nie została zakończona."
            },
            status=400
        )

    # =========================
    # MARK ORDER AS PAID
    # =========================

    order.paid = True

    order.save(
        update_fields=[
            "paid"
        ]
    )

    print(
        f"PayPal payment completed: "
        f"Order #{order.id}, "
        f"PayPal ID: {paypal_order_id}"
    )

    return JsonResponse(
        {
            "success": True,
            "redirect_url": "/sklep/payment-success/"
        }
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