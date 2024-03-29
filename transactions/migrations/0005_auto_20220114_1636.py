# Generated by Django 3.2.8 on 2022-01-14 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_auto_20220114_1600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='Discount',
            new_name='discount',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='GrandTotal',
            new_name='grandtotal',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='InvoiceDate',
            new_name='invoice_date',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='ShipmentCost',
            new_name='shipment_cost',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='SubTotal',
            new_name='subtotal',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='Tax',
            new_name='tax',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='OrderPrice',
            new_name='order_price',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='Quantity',
            new_name='quantity',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='UnitPrice',
            new_name='unit_price',
        ),
    ]
