import requests

from django.conf import settings
from django.urls import reverse


def get_paypal_access_token():

    url = f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"

    response = requests.post(
        url,

        auth=(
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_SECRET
        ),

        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },

        data={
            "grant_type": "client_credentials"
        }
    )

    data = response.json()

    return data["access_token"]


def create_paypal_order(request, product):

    access_token = get_paypal_access_token()

    url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    data = {

        "intent": "CAPTURE",

        "purchase_units": [
            {
                "amount": {
                    "currency_code": "PLN",
                    "value": str(product.price)
                },

                "description": product.name
            }
        ],

        "application_context": {

            "return_url": request.build_absolute_uri(
                reverse("paypal-success")
            ),

            "cancel_url": request.build_absolute_uri(
                reverse("paypal-cancel")
            )
        }
    }

    response = requests.post(
        url,
        json=data,
        headers=headers
    )

    return response.json()