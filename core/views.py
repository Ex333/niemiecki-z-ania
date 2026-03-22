from django.shortcuts import render
from django.http import HttpResponse
from .models import HomePage


def home(request):
    homepage = HomePage.objects.first()
    return render(request, 'home.html', {'homepage': homepage})


def materialy(request):
    return render(request, "materialy.html")

def kontakt(request):
    return render(request, "kontakt.html")