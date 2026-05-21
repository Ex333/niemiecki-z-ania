from django.urls import path

from .views import (
    sklep,
    product_detail,
    create_order,
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
]