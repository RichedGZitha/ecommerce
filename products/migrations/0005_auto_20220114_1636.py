# Generated by Django 3.2.8 on 2022-01-14 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20220108_1706'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Categories',
            new_name='categories',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='FrontImage',
            new_name='front_image',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='FullDescription',
            new_name='full_description',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='isActive',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='isFeatured',
            new_name='is_featured',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='isSpecial',
            new_name='is_special',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Price',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Quantity',
            new_name='quantity',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='RearImage',
            new_name='rear_image',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Specifications',
            new_name='specifications',
        ),
        migrations.RenameField(
            model_name='productreview',
            old_name='starsCount',
            new_name='stars_count',
        ),
    ]
