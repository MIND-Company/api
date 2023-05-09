from django.contrib import admin
from .models import Park, ParkingInfo, Car, Price, ConfirmationCode

admin.site.register(Park)
admin.site.register(ParkingInfo)
admin.site.register(Car)
admin.site.register(Price)
admin.site.register(ConfirmationCode)
