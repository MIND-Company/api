from action_serializer import ModelActionSerializer
from .models import ParkingInfo, Park, Price
from rest_framework import serializers
from datetime import datetime
from pytz import utc


# TODO разобраться насколько грамотно использовать такие вспомогательные сериализаторы
class AuxParkingSerializer(ModelActionSerializer):

    class Meta:
        model = ParkingInfo
        fields = ['car', 'entry_time_utc', 'checkout_time_utc', 'calculated_price']


class AuxParkSerializer(ModelActionSerializer):

    class Meta:
        model = Park
        fields = ['id', 'description', 'web_address']

class AuxPriceSerializer(ModelActionSerializer):

    class Meta:
        model = Price
        fields = ['day_of_week', 'price_per_hour', 'max_price_per_day', 'free_time_in_minutes']

class AuxDateTimeSerializer(serializers.RelatedField):
    def to_representation(self, value: datetime):
        return value.strftime('%d.%m.%Y %H:%M:%S')