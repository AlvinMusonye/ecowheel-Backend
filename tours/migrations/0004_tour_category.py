# Generated by Django 5.2.1 on 2025-06-05 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0003_alter_tour_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='category',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
