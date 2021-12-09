from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import migrations
from django.utils import timezone


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    def generate_superuser(apps, schema_editor):
        user_model = get_user_model()

        superuser = user_model.objects.create_superuser(
            username=settings.DJANGO_SU_NAME,
            email=settings.DJANGO_SU_EMAIL,
            last_login=timezone.now(),
            password=settings.DJANGO_SU_PASSWORD)

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]