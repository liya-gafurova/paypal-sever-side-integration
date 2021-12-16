from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from finance.serializers import BuyPowerPointsSerializer
from finance.domain.service import create_purchase_order, capture_purchase_status, \
     update_payment_transaction_status


class PaypalCreateOrder(generics.CreateAPIView):
    serializer_class = BuyPowerPointsSerializer

    def post(self, request, *args, **kwargs):
        power_points_to_buy = int(request.data.get('power_points_amount', 10000))
        user_id = request.user.id
        payment_id = create_purchase_order(user_id, power_points_to_buy)

        return Response({"id": payment_id}, status=status.HTTP_201_CREATED)


class PaypalCaptureOrder(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        payment_id = kwargs.get('order_id', None)
        result = capture_purchase_status(payment_id)

        return Response({"result": result}, status=status.HTTP_202_ACCEPTED)


class PaypalIPN(generics.CreateAPIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        update_payment_transaction_status(request.data)
        print(request.data)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

