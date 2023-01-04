from django.db import models
from parkingAuth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


class DayOfWeek:

    ALL = "All"
    WEEKEND = "Wkd"

    MONDAY = "Mon"
    THUESDAY = "Tue"
    WEDNESDAY = "Wed"
    THURSDAY = "Thu"
    FRIDAY = "Fri"
    SATURDAY = "Sat"
    SUNDAY = "Sun"

    DAY_NUMBER_TO_DAY = {0: MONDAY, 1: THUESDAY, 2: WEDNESDAY,
                         3: THURSDAY, 4: FRIDAY, 5: SATURDAY, 6: SUNDAY}

    def is_weekend(day):
        return day is "Sun" or day is "Sat"


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
    entry_time_utc = models.DateTimeField()
    checkout_time_utc = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    timezone = models.CharField(max_length=100)
    calculated_price = models.DecimalField(
        max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    park = models.ForeignKey(Park, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'park: {self.park}, car: {self.car}'


class Price(models.Model):

    DAY_OF_WEEK_CHOICES = [
        (DayOfWeek.ALL, "All"),
        (DayOfWeek.WEEKEND, "Weekend"),

        (DayOfWeek.MONDAY, "Monday"),
        (DayOfWeek.THUESDAY, "Thuesday"),
        (DayOfWeek.WEDNESDAY, "Wednesday"),
        (DayOfWeek.THURSDAY, "Thursday"),
        (DayOfWeek.FRIDAY, "Friday"),
        (DayOfWeek.SATURDAY, "Saturday"),
        (DayOfWeek.SUNDAY, "Sunday")
    ]
    day_of_week = models.CharField(
        max_length=3, choices=DAY_OF_WEEK_CHOICES)
    price_per_hour = models.DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    max_price_per_day = models.DecimalField(max_digits=9, decimal_places=2, validators=[
                                            MinValueValidator(0)], null=True, blank=True)
    free_time_in_minutes = models.IntegerField()
    park = models.ForeignKey(Park, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.park} - {self.day_of_week} : {self.price_per_hour}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['park', 'day_of_week'], name="unique week day")
        ]
