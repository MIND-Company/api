# Generated by Django 4.1.1 on 2022-10-03 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkingAuth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]