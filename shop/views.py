import json

from datetime import timedelta

from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from django.core.paginator import Paginator

from django.http import (
    HttpResponse,
    FileResponse
)

from django.views.decorators.csrf import csrf_exempt

from django.core.mail import send_mail

from django.conf import settings

from django.utils import timezone

from .models import (
    Product,
    Order,
    DownloadToken
)

from .paypal import create_paypal_order


# =========================
# SHOP
# =========================

def sklep(request):

    products = Product.objects.filter(
        available=True
    ).order_by("name")

    paginator = Paginator(products, 9)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(request, "shop/sklep.html", {
        "page_obj": page_obj
    })


# =========================
# PRODUCT DETAIL
# =========================

def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        available=True
    )

    return render(
        request,
        "shop/product_detail.html",
        {
            "product": product
        }
    )


# =========================
# CREATE PAYPAL CHECKOUT
# =========================

def create_checkout(request, slug):

    if request.method != "POST":

        return HttpResponse(
            "Nieprawidłowe żądanie.",
            status=400
        )

    product = get_object_or_404(
        Product,
        slug=slug,
        available=True
    )

    # email from form
    customer_email = request.POST.get("email")

    if not customer_email:

        return HttpResponse(
            "Brak adresu email.",
            status=400
        )

    # create paypal order
    paypal_order = create_paypal_order(
        request,
        product
    )

    print(paypal_order)

    # safety check
    if "id" not in paypal_order:

        return HttpResponse(
            "Błąd PayPal.",
            status=500
        )

    paypal_order_id = paypal_order["id"]

    # save order in DB
    Order.objects.create(
        product=product,
        email=customer_email,
        paypal_order_id=paypal_order_id
    )

    # paypal approve url
    approve_url = None

    for link in paypal_order.get("links", []):

        if link.get("rel") == "approve":

            approve_url = link.get("href")
            break

    if not approve_url:

        return HttpResponse(
            "Brak linku PayPal.",
            status=500
        )

    return redirect(approve_url)


# =========================
# PAYPAL SUCCESS
# =========================

def paypal_success(request):

    return HttpResponse(
        "Płatność zakończona. Oczekiwanie na potwierdzenie PayPal..."
    )


# =========================
# PAYPAL CANCEL
# =========================

def paypal_cancel(request):

    return HttpResponse(
        "Płatność anulowana."
    )


# =========================
# PAYPAL WEBHOOK
# =========================

@csrf_exempt
def paypal_webhook(request):

    if request.method != "POST":

        return HttpResponse(status=400)

    try:

        data = json.loads(request.body)

    except json.JSONDecodeError:

        return HttpResponse(status=400)

    print(data)

    event_type = data.get("event_type")

    # successful payment
    if event_type == "CHECKOUT.ORDER.APPROVED":

        resource = data.get("resource", {})

        paypal_order_id = resource.get("id")

        if not paypal_order_id:

            return HttpResponse(status=400)

        try:

            order = Order.objects.get(
                paypal_order_id=paypal_order_id
            )

        except Order.DoesNotExist:

            print("ORDER NOT FOUND")

            return HttpResponse(status=404)

        # already paid protection
        if order.paid:

            return HttpResponse(status=200)

        # mark as paid
        order.paid = True
        order.save()

        # create secure token
        token = DownloadToken.objects.create(
            order=order,

            expires_at=timezone.now() + timedelta(days=3)
        )

        # secure download url
        download_url = request.build_absolute_uri(
            f"/shop/download/{token.token}/"
        )

        # send automatic email
        send_mail(
            subject="Twój zakup - Niemiecki z Anią",

            message=(
                f"Dziękujemy za zakup!\n\n"
                f"Pobierz materiał tutaj:\n\n"
                f"{download_url}\n\n"
                f"Link ważny przez 3 dni."
            ),

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[order.email],

            fail_silently=False,
        )

        print("EMAIL SENT")

    return HttpResponse(status=200)


# =========================
# SECURE DOWNLOAD
# =========================

def secure_download(request, token):

    token_obj = get_object_or_404(
        DownloadToken,
        token=token
    )

    # expired token
    if not token_obj.is_valid():

        return HttpResponse(
            "Link wygasł."
        )

    order = token_obj.order

    # unpaid order
    if not order.paid:

        return HttpResponse(
            "Płatność nie została potwierdzona."
        )

    product_file = order.product.file

    # missing file
    if not product_file:

        return HttpResponse(
            "Brak pliku."
        )

    return FileResponse(
        product_file.open("rb"),
        as_attachment=True
    )