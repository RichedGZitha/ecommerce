# Generated by Django 3.2.8 on 2021-11-02 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='manager',
            new_name='managerOrMerchant',
        ),
    ]
