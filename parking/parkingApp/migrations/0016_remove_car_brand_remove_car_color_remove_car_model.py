# Generated by Django 4.1.1 on 2023-05-09 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingApp', '0015_confirmationcode_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='car',
            name='color',
        ),
        migrations.RemoveField(
            model_name='car',
            name='model',
        ),
    ]
