# Generated by Django 3.2.8 on 2022-01-24 17:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20220114_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='contact',
            new_name='contact_number',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, max_length=256, null=True, validators=[django.core.validators.MaxLengthValidator]),
        ),
    ]
