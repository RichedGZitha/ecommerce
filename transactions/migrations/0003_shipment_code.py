# Generated by Django 3.2.8 on 2022-01-08 15:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_invoice_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='Code',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
