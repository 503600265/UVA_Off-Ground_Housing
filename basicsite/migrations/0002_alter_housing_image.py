# Generated by Django 3.2.7 on 2021-11-12 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housing',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='images'),
        ),
    ]