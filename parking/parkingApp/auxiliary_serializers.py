from action_serializer import ModelActionSerializer
from .models import ParkingInfo, Park

# TODO разобраться насколько грамотно использовать такие вспомогательные сериализаторы
class AuxParkingSimpleSerializer(ModelActionSerializer):

    class Meta:
        model = ParkingInfo
        fields = ['car', 'entry_time', 'checkout_time', 'calculated_price']


class AuxParkSerializer(ModelActionSerializer):

    class Meta:
        model = Park
        fields = ['id', 'description', 'webAddress']
