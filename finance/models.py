from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db.models import ForeignKey, FloatField, DateTimeField, JSONField, CharField, IntegerField, SET_NULL
from django.db.models.signals import pre_save
from django.dispatch import receiver
from ruamel.yaml import timestamp

from finance.domain.business_rules import TransactionTypes

from jsonschema import validate, ValidationError
from rest_framework import serializers

TRANSACTION_DESCRIPTION_FIELD_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "object",
    "title": "transaction_description",

    "required": [
        "message"
    ],
    "properties": {
        "data": {
            "type": "object",
        },
        "message": {
            "type": "string",
        }
    },
}

UserModel = get_user_model()


def validate_json_filed(value):
    try:
        validate(value, TRANSACTION_DESCRIPTION_FIELD_SCHEMA)
    except ValidationError as e:
        raise serializers.ValidationError(e)


class Transaction(models.Model):
    user = ForeignKey(UserModel, null=True, on_delete=models.SET_NULL)
    amount = FloatField()
    timestamp = DateTimeField(auto_now_add=True)
    transaction_type = CharField(max_length=30, null=False, default=TransactionTypes.NOT_DEFINED.value)

    metadata = JSONField(validators=[validate_json_filed], default=dict, blank=True)


class PaymentSystemTransaction(models.Model):
    user = ForeignKey(UserModel, null=True, on_delete=models.SET_NULL)
    order_id = CharField(max_length=50, null=True)
    capture_id = CharField(max_length=50, null=True)

    money_amount = FloatField()
    money_currency = CharField(max_length=10)

    pp_amount = IntegerField()

    status = CharField(max_length=50)

    timestamp = DateTimeField(auto_now_add=True)


class IPNNotifications(models.Model):
    payment = ForeignKey(PaymentSystemTransaction, null=True, on_delete=SET_NULL)
    order_id = CharField(max_length=50, null=True)
    status = CharField(max_length=50)
    notification_data = JSONField()
