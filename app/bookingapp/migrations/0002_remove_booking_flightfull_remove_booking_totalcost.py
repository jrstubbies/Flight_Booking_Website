# Generated by Django 5.0.5 on 2024-05-09 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='flightFull',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='totalCost',
        ),
    ]
