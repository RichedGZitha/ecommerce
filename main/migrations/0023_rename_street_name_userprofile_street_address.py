# Generated by Django 3.2.8 on 2022-01-24 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20220124_1935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='street_name',
            new_name='street_address',
        ),
    ]
