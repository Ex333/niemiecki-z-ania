from django.urls import path

from .views import (
    sklep,
    product_detail,
    create_order,
    payment_success,
    payment_cancel,
)

urlpatterns = [

    # =========================
    # SHOP
    # =========================

    path(
        "",
        sklep,
        name="sklep"
    ),

    path(
        "<slug:slug>/",
        product_detail,
        name="product_detail"
    ),

    path(
        "order/<slug:slug>/",
        create_order,
        name="create_order"
    ),

    # =========================
    # PAYPAL
    # =========================

    path(
        "payment-success/",
        payment_success,
        name="payment_success"
    ),

    path(
        "payment-cancel/",
        payment_cancel,
        name="payment_cancel"
    ),
]