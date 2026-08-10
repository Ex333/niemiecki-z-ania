from django.urls import path

from .views import (
    sklep,
    product_detail,
    create_order,
    capture_order,
    payment_success,
    payment_cancel,
)


urlpatterns = [

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

    path(
        "order/<slug:slug>/",
        create_order,
        name="create_order"
    ),

    path(
        "capture-order/",
        capture_order,
        name="capture_order"
    ),

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
]