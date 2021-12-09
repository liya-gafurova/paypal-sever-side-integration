from django.urls import path, include

from finance.views import PaypalCreateOrder, PaypalCaptureOrder

paypal_url_patterns = [
    path('api/v1/finance/paypal/order/create/', PaypalCreateOrder.as_view(), name="Special paypal ULR, Create Order"),
    path('api/v1/finance/paypal/order/<str:order_id>/capture/', PaypalCaptureOrder.as_view(),
         name="Special Paypal URL, Capture Order"),
]
