from rest_framework import serializers, validators
from action_serializer import ModelActionSerializer
from .auxiliary_serializers import AuxParkingSerializer, AuxParkSerializer, AuxDateTimeSerializer
from .models import Park, ParkingInfo, Car, Price
import pytz
from . import functions
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder



class ParkSerializer(ModelActionSerializer):

    taken = serializers.SerializerMethodField("taken_place_count")
    cars = serializers.SerializerMethodField("cars_list")
    price_list = serializers.SerializerMethodField("get_price_list")

    # TODO подумать над оптимизацией, сейчас 2 вычисляемых поля перебирают список info 2 раза
    def taken_place_count(self, obj):
        infos = obj.parkinginfo_set.all()
        return sum(1 for info in infos if not info.checkout_time)

    def cars_list(self, obj):
        infos = obj.parkinginfo_set.all()
        cars = [AuxParkingSerializer(info).data for info in infos]
        return cars

    def get_price_list(self, obj):
        prices = obj.price_set.all()
        return [PriceSerializer(price).data for price in prices]

    class Meta:
        model = Park
        fields = ['description', 'place_count', 'address',
                  'web_address', 'taken', 'cars', 'id', 'latitude', 'longitude', 'price_list']
        action_fields = {"list": {"fields": ['id', 'description', 'address', 'latitude', 'longitude', 'price_list']},
                         "post": {"fields": ['description', 'latitude', 'longitude', 'price_list', 'owner']}}


class PriceSerializer(ModelActionSerializer):

    park_id = serializers.IntegerField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner = serializers.IntegerField(required=True)

    def validate_park_id(self, value):
        park = Park.objects.get(pk=value)
        if park.owner != self.context['request'].user:
            raise serializers.ValidationError(
                f"park with park_id={value} not found")
        return value

    class Meta:
        model = Price
        fields = ['day_of_week', 'price_per_hour',
                  'max_price_per_day', 'free_time_in_minutes', 'id', 'park_id']

        validators = [validators.UniqueTogetherValidator(
            queryset=Price.objects.all(),
            fields=['park_id', 'day_of_week']
        )]


class CarSerializer(ModelActionSerializer):

    class Meta:
        model = Car
        fields = ['number', 'brand', 'model', 'color']


class ParkingInfoSerializer(ModelActionSerializer):

    park = AuxParkSerializer(many=False, read_only=True)
    entry_time_local = serializers.SerializerMethodField('get_local_entry_time')
    checkout_time_local = serializers.SerializerMethodField('get_local_checkout_time')
    current_price = serializers.SerializerMethodField('calculate_price')

    def get_local_entry_time(self, obj):
        timezone = pytz.timezone(obj.timezone)
        time = obj.entry_time_utc.astimezone(timezone)
        return time

    def get_local_checkout_time(self, obj):
        if not obj.checkout_time_utc:
            return None
        timezone = pytz.timezone(obj.timezone)
        time = obj.checkout_time_utc.astimezone(timezone)
        return time

    def calculate_price(self, obj):
        return str(functions.calculate_price(obj))

    class Meta:
        model = ParkingInfo
        fields = ['car', 'entry_time_utc', 'entry_time_local', 'checkout_time_utc', 'checkout_time_local',
                  'calculated_price', 'current_price', 'park']

class ParkingInfoCreateSerializer(ModelActionSerializer):

    entry_time_local = serializers.SerializerMethodField('get_local_entry_time')
    checkout_time_local = serializers.SerializerMethodField('get_local_checkout_time')

    def get_local_entry_time(self, obj):
        timezone = pytz.timezone(obj.timezone)
        time = obj.entry_time_utc.astimezone(timezone)
        return time

    def get_local_checkout_time(self, obj):
        if not obj.checkout_time_utc:
            return None
        timezone = pytz.timezone(obj.timezone)
        time = obj.checkout_time_utc.astimezone(timezone)
        return time

    def validate_car(self, car):
        infos = ParkingInfo.objects.filter(car=car, checkout_time_utc=None)
        if len(infos) > 0:
            raise serializers.ValidationError(f'Машина с номером {car.number} уже находится на парковке')
        return car

    def save(self, **kwargs):
        kwargs['entry_time_utc'] = datetime.now(pytz.timezone('UTC'))
        tf = TimezoneFinder()
        park = self.validated_data['park']
        timezone = tf.timezone_at(lng=park.longitude, lat=park.latitude)
        kwargs['timezone'] = timezone
        return super().save(**kwargs)

    class Meta:
        model = ParkingInfo
        fields = ['car', 'park', 'entry_time_local', 'entry_time_utc', 'checkout_time_local', 'checkout_time_utc']
        read_only_fields = ['entry_time_utc']
