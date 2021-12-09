import json
import sys
from urllib.parse import quote

from django.conf import settings
from paypalcheckoutsdk.core import SandboxEnvironment, PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersCreateRequest


class OrdersCreateRequest:
    """
    Creates an order.
    """

    def __init__(self):
        self.verb = "POST"
        self.path = "/v2/checkout/orders?"
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None

    def pay_pal_partner_attribution_id(self, pay_pal_partner_attribution_id):
        self.headers["PayPal-Partner-Attribution-Id"] = str(pay_pal_partner_attribution_id)

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)

    def request_body(self, order):
        self.body = order
        return self


class OrdersCaptureRequest:
    """
    Captures a payment for an order.
    """

    def __init__(self, order_id):
        self.verb = "POST"
        self.path = "/v2/checkout/orders/{order_id}/capture?".replace("{order_id}", quote(str(order_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None

    def pay_pal_client_metadata_id(self, pay_pal_client_metadata_id):
        self.headers["PayPal-Client-Metadata-Id"] = str(pay_pal_client_metadata_id)

    def pay_pal_request_id(self, pay_pal_request_id):
        self.headers["PayPal-Request-Id"] = str(pay_pal_request_id)

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)


class PayPalClient:
    def __init__(self):
        self.client_id = settings.CLIENT_ID
        self.client_secret = settings.CLIENT_SECRET

        """Setting up and Returns PayPal SDK environment with PayPal Access credentials.
           For demo purpose, we are using SandboxEnvironment. In production this will be
           LiveEnvironment."""
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment which has access
            credentials context. This can be used invoke PayPal API's provided the
            credentials have the access to do so. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = iter(json_data.__dict__.items())
        else:
            itr = list(json_data.__dict__.items())
        for key, value in itr:
            # Skip internal attributes.
            if key.startswith("__") or key.startswith("_"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else \
                self.object_to_json(value) if not self.is_primittive(value) else \
                    value
        return result

    def array_to_json_array(self, json_array):
        result = []
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if not self.is_primittive(item) \
                                  else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result;

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, str) or isinstance(data, int)


class PaypalCreateOrder(PayPalClient):

    @staticmethod
    def build_request_body(user_id, value, currency_code, unit_amount, quantity):

        """Method to create body with CAPTURE intent"""
        return \
            {
                "intent": "CAPTURE",

                "purchase_units": [
                    {
                        "custom_id": str(user_id),
                        "soft_descriptor": f"{quantity} PowerPoints", # DOESN'T RETURN WHILE CAPTURING
                        "amount": {
                            "currency_code": currency_code,
                            "value": str(value),
                        },
                    }
                ]
            }

    """ This is the sample function which can be sued to create an order. It uses the
        JSON body returned by buildRequestBody() to create an new Order."""

    def create_order(self, user_id, currency_code, value, unit_amount, quantity, debug=False):
        request = OrdersCreateRequest()
        request.headers['prefer'] = 'return=representation'
        request_body = self.build_request_body(user_id, value, currency_code, unit_amount, quantity)
        request.request_body(request_body)
        response = self.client.execute(request)
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
            print('Intent: ', response.result.intent)
            print('Links:')
            for link in response.result.links:
                print(('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method)))
            print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                                               response.result.purchase_units[0].amount.value))
            json_data = self.object_to_json(response.result)
            print("json_data: ", json.dumps(json_data, indent=4))
        return response


class PaypalCaptureOrder(PayPalClient):
    """this is the sample function performing payment capture on the order. Approved Order id should be passed as an argument to this function"""

    def capture_order(self, order_id, debug=False):
        """Method to capture order using order_id"""
        request = OrdersCaptureRequest(order_id)
        response = self.client.execute(request)
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
            print('Links: ')
            for link in response.result.links:
                print(('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method)))
            print('Capture Ids: ')
            for purchase_unit in response.result.purchase_units:
                for capture in purchase_unit.payments.captures:
                    print('\t', capture.id)
            print("Buyer:")
            print("\tEmail Address: {}\n\tName: {}\n".format(response.result.payer.email_address,
                                                                               response.result.payer.name.given_name + " " + response.result.payer.name.surname,
                                                                               ))
            json_data = self.object_to_json(response.result)
            print("json_data: ", json.dumps(json_data, indent=4))
        return response


