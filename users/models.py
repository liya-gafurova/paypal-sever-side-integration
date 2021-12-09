from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db.models import OneToOneField, BooleanField, CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver

UserModel = get_user_model()


class UserProfile(models.Model):
    user = OneToOneField(UserModel, null=True, on_delete=CASCADE)
    receive_email = BooleanField(default=True)


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, )
