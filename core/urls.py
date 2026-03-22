from django.urls import path
from .views import home, materialy, kontakt
from core import views


urlpatterns = [
    path("", home, name="home"),
    path("materialy/", materialy, name="materialy"),
    path("kontakt/", kontakt, name="kontakt"),
    path("dziekuje/", views.dziekuje, name="dziekuje"),
]

