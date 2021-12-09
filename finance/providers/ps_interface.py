from dataclasses import dataclass

from finance.providers.paypal import PaypalCreateOrder, PaypalCaptureOrder

'''
Payment System Interface
    current version uses PayPal as a Payment System
'''

@dataclass
class UserPaymentOrder:
    user_id: int
    amount: float
    currency_code: str

    unit_amount: float
    quantity: int

@dataclass
class CreateOrderResponse:
    order_id: str
    status: str

@dataclass
class CaptureOrderResponse:
    order_id: str
    capture_id: str
    status: str

    user_id: int
    actual_amount: float
    currency_code: str


class PaymentInterface:
    create_payment_class = PaypalCreateOrder()
    check_payment_class = PaypalCaptureOrder()

    def create_payment(self, user_payment: UserPaymentOrder):
        response = self.create_payment_class.create_order(user_payment.user_id,
                                                          user_payment.currency_code,
                                                          user_payment.amount,
                                                          user_payment.unit_amount,
                                                          user_payment.quantity,
                                                          debug=True)
        order_id = ''
        print('Creating Order...')
        if response.status_code == 201:
            order_id = response.result.id
            for link in response.result.links:
                print(('\t{} link: {}\tCall Type: {}'.format(str(link.rel).capitalize(), link.href, link.method)))
            print('Created Successfully\n')
            print(
                'Copy approve link and paste it in browser. Login with buyer account and follow the instructions.\nOnce approved hit enter...')
        else:
            print('Link is unreachable')
            exit(1)

        return CreateOrderResponse(order_id = order_id, status=response.result.status)

    def check_payment(self, payment_id):
        capture_id = ""
        user_id = ''
        response = self.check_payment_class.capture_order(payment_id, debug=True)
        if response.status_code == 201:
            print('Captured Successfully\n')
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
            print('Capture Ids: ')
            for purchase_unit in response.result.purchase_units:
                for capture in purchase_unit.payments.captures:
                    print('\t', capture.id)
                    capture_id = capture.id
            print('Links: ')

            for link in response.result.links:
                print(('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method)))

            print('---------------------')


        return CaptureOrderResponse(capture_id=capture_id,
                                    order_id=response.result.id,
                                    status = response.result.status,
                                    user_id=int(response.result.purchase_units[0].payments.captures[0].custom_id),
                                    actual_amount=float(response.result.purchase_units[0].payments.captures[0].amount.value),
                                    currency_code=response.result.purchase_units[0].payments.captures[0].amount.currency_code
                                    )
