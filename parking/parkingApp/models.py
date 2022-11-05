from django.db import models
from parkingAuth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Car(models.Model):
    number = models.CharField(max_length=9, primary_key=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Park(models.Model):
    description = models.CharField(max_length=128)
    place_count = models.IntegerField(validators=[
        MinValueValidator(
            1, "Количество мест не может быть отрицательным и меньше 1"),
        MaxValueValidator(10_001, "Таких больших парковок не бывает")])
    address = models.CharField(max_length=512)
    webAddress = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)


class ParkingInfo(models.Model):
    entry_time = models.DateTimeField(auto_now_add=True)
    checkout_time = models.DateTimeField(auto_now_add=False, null=True)
    calculated_price = models.DecimalField(
        max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], null=True)
    park = models.ForeignKey(Park, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
