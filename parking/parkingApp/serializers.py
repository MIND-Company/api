from rest_framework import serializers
from action_serializer import ModelActionSerializer
from .models import Park, ParkingInfo, Car


class ParkSerializer(ModelActionSerializer):

    taken = serializers.SerializerMethodField("taken_place_count")
    cars = serializers.SerializerMethodField("cars_list")

    # TODO подумать над оптимизацией, сейчас 2 вычисляемых поля перебирают список info 2 раза
    def taken_place_count(self, obj):
        infos = obj.parkinginfo_set.all()
        return sum(1 for info in infos if not info.checkout_time)

    def cars_list(sekf, obj):
        infos = obj.parkinginfo_set.all()
        cars = [ParkingInfoSerializer(info).data for info in infos]
        return cars

    class Meta:
        model = Park
        fields = ['description', 'place_count', 'address',
                  'webAddress', 'taken', 'cars', 'id']
        action_fields = {"list": {"fields": ['id', 'description', 'address']}}


class CarSerializer(ModelActionSerializer):

    class Meta:
        model = Car
        fields = ['number', 'brand', 'model', 'color']


class ParkingInfoSerializer(ModelActionSerializer):

    class Meta:
        model = ParkingInfo
        fields = ['car', 'entry_time', 'checkout_time', 'calculated_price']
