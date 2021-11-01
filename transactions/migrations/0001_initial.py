# Generated by Django 3.2.8 on 2021-10-31 12:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_alter_product_categories'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('Discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('ShipmentCost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('SubTotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('GrandTotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('InvoiceDate', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ShipmentDate', models.DateTimeField(auto_now_add=True)),
                ('ShipmentCost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('Address', models.TextField()),
                ('isArrived', models.BooleanField(default=False)),
                ('Phone', models.CharField(max_length=20, validators=[django.core.validators.MaxLengthValidator])),
                ('Email', models.EmailField(max_length=254)),
                ('Firstname', models.CharField(max_length=100, validators=[django.core.validators.MaxLengthValidator])),
                ('Lastname', models.CharField(max_length=100, validators=[django.core.validators.MaxLengthValidator])),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(default=0)),
                ('UnitPrice', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('OrderPrice', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.invoice')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
        ),
    ]
