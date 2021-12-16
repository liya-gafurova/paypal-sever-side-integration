from django.urls import path, include

from finance.views import PaypalCreateOrder, PaypalCaptureOrder, PaypalIPN

finance_url_patterns = [
    path('api/v1/finance/paypal/order/create/', PaypalCreateOrder.as_view(), name="Special paypal ULR, Create Order"),
    path('api/v1/finance/paypal/order/<str:order_id>/capture/', PaypalCaptureOrder.as_view(), name="Special Paypal URL, Capture Order"),
    path('api/v1/finance/paypal/ipn/', PaypalIPN.as_view(), name="Paypal IPN"),
]

# http://localhost:8000/api/v1/finance/paypal/ipn/ -- webhook to get IPN data
