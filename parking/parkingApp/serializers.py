from rest_framework import serializers
from action_serializer import ModelActionSerializer
from .auxiliary_serializers import AuxParkingSerializer, AuxParkSerializer, AuxDateTimeSerializer
from .models import Park, ParkingInfo, Car
import pytz
from . import functions


class ParkSerializer(ModelActionSerializer):

    taken = serializers.SerializerMethodField("taken_place_count")
    cars = serializers.SerializerMethodField("cars_list")

    # TODO подумать над оптимизацией, сейчас 2 вычисляемых поля перебирают список info 2 раза
    def taken_place_count(self, obj):
        infos = obj.parkinginfo_set.all()
        return sum(1 for info in infos if not info.checkout_time)

    def cars_list(self, obj):
        infos = obj.parkinginfo_set.all()
        cars = [AuxParkingSerializer(info).data for info in infos]
        return cars

    class Meta:
        model = Park
        fields = ['description', 'place_count', 'address',
                  'web_address', 'taken', 'cars', 'id', 'latitude', 'longitude']
        action_fields = {"list": {"fields": ['id', 'description', 'address', 'latitude', 'longitude']}, 
        "post": {"fields": ['description', 'latitude', 'longitude', 'owner']}}


class CarSerializer(ModelActionSerializer):

    class Meta:
        model = Car
        fields = ['number', 'brand', 'model', 'color']


class ParkingInfoSerializer(ModelActionSerializer):

    park = AuxParkSerializer(many=False, read_only=True)
    entry_time_utc = AuxDateTimeSerializer(many = False, read_only = True)
    entry_time = serializers.SerializerMethodField('get_local_entry_time')
    checkout_time = serializers.SerializerMethodField('get_local_checkout_time')
    current_price = serializers.SerializerMethodField('calculate_price')


    def get_local_entry_time(self, obj):
        timezone = pytz.timezone(obj.timezone)
        time = obj.entry_time_utc.astimezone(timezone)
        return time.strftime('%d.%m.%Y %H:%M:%S')

    def get_local_checkout_time(self, obj):
        if not obj.checkout_time_utc:
            return None
        timezone = pytz.timezone(obj.timezone)
        time = obj.checkout_time_utc.astimezone(timezone)
        return time.strftime('%d.%m.%Y %H:%M:%S')
    
    def calculate_price(self, obj):
        return str(functions.calculate_price(obj))

    class Meta:
        model = ParkingInfo
        fields = ['car', 'entry_time_utc', 'checkout_time_utc', 'entry_time', 'checkout_time',
                  'calculated_price', 'current_price', 'park']

