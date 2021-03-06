# Generated by Django 3.2.9 on 2021-12-09 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentSystemTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=50, null=True)),
                ('capture_id', models.CharField(max_length=50, null=True)),
                ('money_amount', models.FloatField()),
                ('money_currency', models.CharField(max_length=10)),
                ('pp_amount', models.IntegerField()),
                ('status', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
