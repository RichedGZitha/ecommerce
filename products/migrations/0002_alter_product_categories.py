# Generated by Django 3.2.8 on 2021-10-30 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Categories',
            field=models.ManyToManyField(blank=True, related_name='productCategories', to='products.Category'),
        ),
    ]
