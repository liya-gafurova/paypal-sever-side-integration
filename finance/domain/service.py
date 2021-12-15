from dataclasses import dataclass
from typing import List

from finance.domain.business_rules import PP_USD, USD, USD_VALUE_DECIMAL_PLACES, DOLLARS_PER_POWER_POINT, \
    TransactionTypes, PaymentSystemTransactionStatus
from finance.models import PaymentSystemTransaction, Transaction
from finance.providers.db_interface import DB_Creator, DB_Selector, DB_Updater
from finance.providers.paypal import PaypalIPNStatus, PaypalPaymentStatus, IPN_Paypal_status_mapping
from finance.providers.ps_interface import PaymentInterface, UserPaymentOrder, CreateOrderResponse, CaptureOrderResponse


def _get_dollars(power_points_amount):
    dollars_per_power_point = PP_USD.first_second_rate
    dollars_float = power_points_amount * dollars_per_power_point
    dollars_and_cents = round(dollars_float, USD_VALUE_DECIMAL_PLACES)
    return dollars_and_cents


def create_purchase_order(user_id, power_points_amount: int):
    payment_system = PaymentInterface()

    dollars_amount = _get_dollars(power_points_amount)
    user_payment = UserPaymentOrder(user_id=user_id,
                                    amount=dollars_amount,
                                    currency_code=USD.name,
                                    unit_amount=DOLLARS_PER_POWER_POINT,
                                    quantity=power_points_amount)
    created_order_response: CreateOrderResponse = payment_system.create_payment(user_payment)

    DB_Creator.create_payment_system_transaction(user=user_id,
                                                 order_id=created_order_response.order_id,
                                                 money_amount=dollars_amount,
                                                 money_currency=USD.name,
                                                 pp_amount=power_points_amount,
                                                 status=created_order_response.status)

    return created_order_response.order_id


def _created_order_is_same_as_captured_order(capture_response: CaptureOrderResponse,
                                             created_order_transaction: PaymentSystemTransaction):
    '''
    :return: True if created order in paypal has the same value and amount after User`s approving payment, else False
    '''

    return capture_response.currency_code == created_order_transaction.money_currency \
           and capture_response.actual_amount == created_order_transaction.money_amount


def capture_purchase_status(payment_id):
    payment_system = PaymentInterface()

    captured_order_response: CaptureOrderResponse = payment_system.check_payment(payment_id)
    created_order_paypal_transaction = DB_Selector.get_payment_transaction_by_order_id(captured_order_response.order_id)

    if _created_order_is_same_as_captured_order(captured_order_response, created_order_paypal_transaction):
        if captured_order_response.status == PaymentSystemTransactionStatus.COMPLETED.value:
            # update payment system transaction
            updated_ps_transaction: PaymentSystemTransaction = DB_Updater.update_payment_transaction_status(
                captured_order_response.order_id,
                captured_order_response.capture_id,
                captured_order_response.status)

            # add pp transaction
            transaction_metadata: dict = {
                'message': f'User bought {updated_ps_transaction.pp_amount} PowerPoints with '
                           f'{updated_ps_transaction.money_amount} {updated_ps_transaction.money_currency} '
                           f'via PayPal payment system.',
                'data': {
                    'money_spent': updated_ps_transaction.money_amount,
                }
            }
            pp_transaction: Transaction = DB_Creator.create_pp_transaction(user=updated_ps_transaction.user,
                                                                           amount=updated_ps_transaction.pp_amount,
                                                                           transaction_type=TransactionTypes.BUYING_POWERPOINTS.value,
                                                                           metadata=transaction_metadata)

        return captured_order_response.capture_id

    return None


def update_payment_transaction_status(paypal_ipn_data: dict):
    print(paypal_ipn_data.get('event_type', None))
    ipn_status = paypal_ipn_data.get('event_type', None)
    if ipn_status == PaypalIPNStatus.COMPLETED.value:
        ccl_user_id = paypal_ipn_data['resource']['custom_id']
        order_id = paypal_ipn_data['resource']['supplementary_data']["related_ids"]["order_id"]

        order_paypal_transaction = DB_Selector.get_payment_transaction_by_order_id(order_id)
        print(order_paypal_transaction.order_id, order_paypal_transaction.capture_id, order_paypal_transaction.status,)

        if order_paypal_transaction.status != IPN_Paypal_status_mapping[ipn_status]:

            print('UPDATE VIA IPN DATA')

            # update payment system transaction
            updated_ps_transaction: PaymentSystemTransaction = DB_Updater.update_payment_transaction_status(
                order_id,
                paypal_ipn_data['resource']['id'],
                PaypalPaymentStatus.COMPLETED)

            # add pp transaction
            transaction_metadata: dict = {
                'message': f'User bought {updated_ps_transaction.pp_amount} PowerPoints with '
                           f'{updated_ps_transaction.money_amount} {updated_ps_transaction.money_currency} '
                           f'via PayPal payment system.',
                'data': {
                    'money_spent': updated_ps_transaction.money_amount,
                }
            }
            pp_transaction: Transaction = DB_Creator.create_pp_transaction(user=updated_ps_transaction.user,
                                                                           amount=updated_ps_transaction.pp_amount,
                                                                           transaction_type=TransactionTypes.BUYING_POWERPOINTS.value,
                                                                           metadata=transaction_metadata)

