# Generated by Django 3.2.7 on 2021-11-25 19:42

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicsite', '0003_alter_housing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housing',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image'),
        ),
    ]
