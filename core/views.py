from django.shortcuts import render
from django.http import HttpResponse
from .models import HomePage
from .forms import ContactForm
from django.shortcuts import redirect


def home(request):
    homepage = HomePage.objects.first()
    return render(request, 'home.html', {'homepage': homepage})


def materialy(request):
    return render(request, "materialy.html")

def kontakt(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]

        print(name, email, message)

        return redirect("dziekuje")

    return render(request, "kontakt.html", {"form": form})

def dziekuje(request):
    return render(request, "dziekuje.html")