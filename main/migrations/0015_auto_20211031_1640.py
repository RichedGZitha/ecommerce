# Generated by Django 3.2.8 on 2021-10-31 14:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_coupon_expireddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='Code',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='expiredDate',
            field=models.DateTimeField(),
        ),
    ]
