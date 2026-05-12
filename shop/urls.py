from django.urls import path

from .views import (
    sklep,
    product_detail,

    create_checkout,

    paypal_success,
    paypal_cancel,
    paypal_webhook,

    secure_download,
)

urlpatterns = [

    # =========================
    # PAYPAL
    # =========================

    path(
        "checkout/<slug:slug>/",
        create_checkout,
        name="create-checkout"
    ),

    path(
        "paypal/success/",
        paypal_success,
        name="paypal-success"
    ),

    path(
        "paypal/cancel/",
        paypal_cancel,
        name="paypal-cancel"
    ),

    path(
        "paypal/webhook/",
        paypal_webhook,
        name="paypal-webhook"
    ),

    # =========================
    # DOWNLOAD
    # =========================

    path(
        "download/<uuid:token>/",
        secure_download,
        name="secure-download"
    ),

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
]