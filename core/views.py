from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import HomePage, Category, Material
from .forms import ContactForm
from django.db.models import Q


def home(request):
    homepage = HomePage.objects.first()
    return render(request, 'home.html', {'homepage': homepage})


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

def material_list(request):
    materials = Material.objects.all().order_by("-created_at")
    categories = Category.objects.all()

    search_query = request.GET.get("search")

    if search_query:
        materials = materials.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    return render(request, "materialy.html", {
        "materials": materials,
        "categories": categories,
    })


def material_detail(request, slug):
    material = get_object_or_404(Material, slug=slug)

    pdf_url = request.build_absolute_uri(material.pdf.url)

    return render(request, "material_detail.html", {
        "material": material,
        "pdf_url": pdf_url
    })


def material_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    materials = Material.objects.filter(category=category)
    categories = Category.objects.all()

    return render(request, "materialy.html", {
        "materials": materials,
        "categories": categories,
        "active_category": category
    })