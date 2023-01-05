from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response
from .serializers import ParkSerializer, ParkingInfoSerializer, CarSerializer, PriceSerializer, ParkingInfoCreateSerializer
from .models import Park, ParkingInfo, Car, Price
from .castom_viewsets import NonReadableViewSet, CreateOnlyViewSet
from datetime import datetime
import pytz
from . import functions


class ParkViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        user = self.request.user
        if not user.id:
            return []
        return Park.objects.filter(owner=user)

    serializer_class = ParkSerializer
    permission_classes = [permissions.IsAuthenticated]


class ParkingInfoViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        user = self.request.user
        if not user.id:
            return []
        user_cars = Car.objects.filter(owner=user)

        infos = [i for i in ParkingInfo.objects.filter(car__in=user_cars)]
        return sorted(infos, key=lambda x: x.entry_time_utc, reverse=True)

    serializer_class = ParkingInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CarViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        if not user.id:
            return []
        return Car.objects.filter(owner=user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]


class PriceViewSet(NonReadableViewSet):

    def get_queryset(self):
        user = self.request.user
        if not user.id:
            return []
        user_parks = Park.objects.filter(owner=user)

        return Price.objects.filter(park__in=user_parks)

    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ParkCreate(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if ('description' not in request.data or len(request.data['description']) < 1):
            response = {
                'description': 'This field is required and may not be blank'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer = ParkSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        park = Park(owner=request.user, **validated_data)
        park.save()
        return Response(validated_data, status=status.HTTP_201_CREATED)


class ParkingRecordViewSet(CreateOnlyViewSet):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ParkingInfoCreateSerializer


class ParkingRecordCheckout(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        errors = {}
        if ('park' not in request.data):
            errors['description'] = 'This field is required'
        if ('car' not in request.data):
            errors['car'] = 'This field is required'
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        car = request.data['car']
        park = request.data['park']
        parking_record = ParkingInfo.objects.filter(
            park_id=park, car_id=car, checkout_time_utc=None).first()
        if not parking_record:
            return Response({'errors': f'entry parking record for car:{car} park:{park} not found'}, status=status.HTTP_400_BAD_REQUEST)

        parking_record.checkout_time_utc = datetime.now(pytz.timezone('UTC'))
        parking_record.calculated_price = functions.calculate_price(
            parking_record)

        parking_record.save()
        json = ParkingInfoCreateSerializer(parking_record)

        return Response(json.data, status=status.HTTP_200_OK)
