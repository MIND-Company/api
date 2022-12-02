from django.db import models
from parkingAuth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


class Car(models.Model):
    number = models.CharField(max_length=9, primary_key=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.number


class Park(models.Model):
    description = models.CharField(
        max_length=128, blank=False, default=None, validators=[MinLengthValidator(1)])
    place_count = models.IntegerField(validators=[
        MinValueValidator(
            1, "Количество мест не может быть отрицательным и меньше 1"),
        MaxValueValidator(10_001, "Таких больших парковок не бывает")])
    address = models.CharField(max_length=512, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    web_address = models.CharField(max_length=128, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.description


class ParkingInfo(models.Model):
    entry_time = models.DateTimeField(auto_now_add=True)
    checkout_time = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    calculated_price = models.DecimalField(
        max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    park = models.ForeignKey(Park, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'park: {self.park}, car: {self.car}'
