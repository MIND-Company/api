# Generated by Django 4.1.1 on 2023-05-08 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkingApp', '0013_confirmationcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkinginfo',
            name='unregistred_car_number',
            field=models.CharField(max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='parkinginfo',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parkingApp.car'),
        ),
    ]
