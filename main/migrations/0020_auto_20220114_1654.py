# Generated by Django 3.2.8 on 2022-01-14 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_customuser_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='Code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='coupon',
            old_name='createdDate',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='coupon',
            old_name='expiredDate',
            new_name='expired_date',
        ),
        migrations.RenameField(
            model_name='coupon',
            old_name='isValid',
            new_name='is_valid',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='Avatar',
            new_name='avatar',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='Biography',
            new_name='biography',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='Contact',
            new_name='contact',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='Country',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='HeaderImage',
            new_name='header_image',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='isManager',
            new_name='is_manager',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='isSeller',
            new_name='is_seller',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='loyaltyPoints',
            new_name='loyalty_points',
        ),
    ]