from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "home.html")


def materialy(request):
    return render(request, "materialy.html")

def kontakt(request):
    return render(request, "kontakt.html")