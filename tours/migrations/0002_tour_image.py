# Generated by Django 5.2.1 on 2025-05-21 10:59

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
