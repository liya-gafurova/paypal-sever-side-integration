from rest_framework import serializers
from rest_framework.fields import FloatField, IntegerField, CharField


class BuyPowerPointsSerializer(serializers.Serializer):
    power_points_amount = IntegerField()