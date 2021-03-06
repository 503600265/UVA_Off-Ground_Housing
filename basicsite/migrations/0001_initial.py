# Generated by Django 3.2.7 on 2021-11-09 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Housing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1000)),
                ('price', models.FloatField()),
                ('address', models.CharField(default='No Address Entered', max_length=1000)),
                ('rating', models.FloatField(null=True)),
                ('ratedYet', models.BooleanField(default=False)),
                ('numReviews', models.IntegerField(default=0)),
                ('numRooms', models.IntegerField(default=0)),
                ('numBathrooms', models.IntegerField(default=0)),
                ('publishDate', models.DateTimeField(null=True, verbose_name='date published')),
                ('startRentalDate', models.CharField(max_length=500, null=True)),
                ('endRentalDate', models.CharField(max_length=500, null=True)),
                ('image', models.ImageField(blank=True, upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.CharField(max_length=2000)),
                ('rating', models.IntegerField()),
                ('housing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicsite.housing')),
            ],
        ),
    ]
