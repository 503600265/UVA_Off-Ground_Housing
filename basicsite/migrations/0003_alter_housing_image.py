# Generated by Django 3.2.7 on 2021-11-13 21:33

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicsite', '0002_alter_housing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housing',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
