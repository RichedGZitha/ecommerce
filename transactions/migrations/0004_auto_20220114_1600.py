# Generated by Django 3.2.8 on 2022-01-14 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_shipment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipment',
            old_name='Code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='shipment',
            old_name='ShipmentCost',
            new_name='cost',
        ),
        migrations.RenameField(
            model_name='shipment',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='shipment',
            old_name='Firstname',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='shipment',
            old_name='isArrived',
            new_name='is_arrived',
        ),
        migrations.RenameField(
            model_name='shipment',
            old_name='Lastname',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='shipment',
            old_name='Phone',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='shipment',
            old_name='ShipmentDate',
            new_name='shipment_date',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='Address',
        ),
    ]