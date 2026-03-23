from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("kontakt/", views.kontakt, name="kontakt"),
    path("dziekuje/", views.dziekuje, name="dziekuje"),

    # 🔥 MATERIAŁY
    path("materialy/", views.material_list, name="material_list"),
    path("materialy/kategoria/<slug:slug>/", views.material_by_category, name="material_by_category"),
    path("materialy/<slug:slug>/", views.material_detail, name="material_detail"),
]

