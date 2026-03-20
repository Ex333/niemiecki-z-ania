from django.urls import path
from .views import home, materialy, kontakt


urlpatterns = [
    path("", home, name="home"),
    path("materialy/", materialy, name="materialy"),
    path("kontakt/", kontakt, name="kontakt"),
]

