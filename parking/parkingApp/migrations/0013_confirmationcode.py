# Generated by Django 4.1.1 on 2023-05-08 13:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('parkingApp', '0012_alter_parkinginfo_park_alter_price_day_of_week_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmationCode',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('car_number', models.CharField(max_length=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
