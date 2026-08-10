from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import HomePage, Category, Material
from .forms import ContactForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
import requests


def home(request):
    homepage = HomePage.objects.first()
    return render(request, "home.html", {"homepage": homepage})


def kontakt(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        # 🛡️ CLOUDFLARE TURNSTILE
        turnstile_token = request.POST.get("cf-turnstile-response")

        if not turnstile_token:
            form.add_error(
                None,
                "Potwierdź, że nie jesteś botem."
            )

            return render(
                request,
                "kontakt.html",
                {
                    "form": form,
                    "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
                },
            )

        # 🔍 WERYFIKACJA TOKENA W CLOUDFLARE
        try:
            turnstile_response = requests.post(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify",
                data={
                    "secret": settings.TURNSTILE_SECRET_KEY,
                    "response": turnstile_token,
                    "remoteip": request.META.get("REMOTE_ADDR"),
                },
                timeout=10,
            )

            turnstile_result = turnstile_response.json()

        except requests.RequestException:
            form.add_error(
                None,
                "Nie udało się zweryfikować zabezpieczenia. Spróbuj ponownie."
            )

            return render(
                request,
                "kontakt.html",
                {
                    "form": form,
                    "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
                },
            )

        # ❌ TURNSTILE ODRZUCIŁ WERYFIKACJĘ
        if not turnstile_result.get("success"):
            form.add_error(
                None,
                "Weryfikacja antybotowa nie powiodła się. Spróbuj ponownie."
            )

            return render(
                request,
                "kontakt.html",
                {
                    "form": form,
                    "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
                },
            )

        # ✅ TURNSTILE OK — DOPIERO TERAZ WYSYŁAMY MAILE

        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]

        # 📩 MAIL DO CIEBIE
        send_mail(
            subject=f"Nowa wiadomość od {name}",
            message=(
                f"Imię: {name}\n"
                f"Email: {email}\n\n"
                f"Wiadomość:\n{message}"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # 📩 AUTO-ODPOWIEDŹ DO UŻYTKOWNIKA
        send_mail(
            subject="Dziękujemy za wiadomość",
            message=f"""Cześć {name},

dziękujemy za wiadomość.
Odpowiemy Ci wkrótce.

Pozdrawiamy
Ania""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect("dziekuje")

    return render(
        request,
        "kontakt.html",
        {
            "form": form,
            "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
        },
    )


def dziekuje(request):
    return render(request, "dziekuje.html")


def material_list(request):
    materials = Material.objects.all().order_by("-created_at")
    categories = Category.objects.all()

    search_query = request.GET.get("search")

    if search_query:
        materials = materials.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__name__icontains=search_query)
        )

    paginator = Paginator(materials, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "materialy.html",
        {
            "page_obj": page_obj,
            "categories": categories,
        },
    )


def material_detail(request, slug):
    material = get_object_or_404(Material, slug=slug)

    pdf_url = request.build_absolute_uri(material.pdf.url)

    return render(
        request,
        "material_detail.html",
        {
            "material": material,
            "pdf_url": pdf_url,
        },
    )


def material_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    materials = Material.objects.filter(category=category)
    categories = Category.objects.all()

    return render(
        request,
        "materialy.html",
        {
            "materials": materials,
            "categories": categories,
            "active_category": category,
        },
    )


def privacy(request):
    return render(request, "legal/privacy.html")


def regulamin(request):
    return render(request, "legal/regulamin.html")


def seller(request):
    return render(request, "legal/seller.html")