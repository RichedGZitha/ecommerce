# Generated by Django 3.2.8 on 2022-01-14 13:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_invoice_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ShipmentDate', models.DateTimeField(auto_now_add=True)),
                ('ShipmentCost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('Address', models.TextField()),
                ('street_name', models.CharField(max_length=500, validators=[django.core.validators.MaxLengthValidator])),
                ('country', models.CharField(max_length=500, validators=[django.core.validators.MaxLengthValidator])),
                ('postal_code', models.CharField(max_length=500, validators=[django.core.validators.MaxLengthValidator])),
                ('province', models.CharField(max_length=500, validators=[django.core.validators.MaxLengthValidator])),
                ('city', models.CharField(max_length=500, validators=[django.core.validators.MaxLengthValidator])),
                ('surburb', models.CharField(blank=True, max_length=500, null=True, validators=[django.core.validators.MaxLengthValidator])),
                ('isArrived', models.BooleanField(default=False)),
                ('Phone', models.CharField(max_length=20, validators=[django.core.validators.MaxLengthValidator])),
                ('Email', models.EmailField(max_length=254)),
                ('Code', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('Firstname', models.CharField(max_length=100, validators=[django.core.validators.MaxLengthValidator])),
                ('Lastname', models.CharField(max_length=100, validators=[django.core.validators.MaxLengthValidator])),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.invoice')),
            ],
        ),
    ]
