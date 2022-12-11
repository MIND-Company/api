from django.shortcuts import render
from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response
from .serializers import ParkSerializer, ParkingInfoSerializer, CarSerializer
from .models import Park, ParkingInfo, Car


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
        print(user_cars)
        infos = [i for i in ParkingInfo.objects.filter(car__in=user_cars)]
        return sorted(infos, key=lambda x: x.entry_time, reverse=True)

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



class ParkingRecord(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        if ('park_id' not in data):
            response = {'park_id': 'This field is required'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if ('car_number' not in data):
            response = {'car_number': 'This field is required'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        park = Park.objects.filter(pk=data["park_id"]).first()
        car = Car.objects.filter(pk=data["car_number"]).first()

        if (park is None):
            response = {
                'park_id': f'Паркинг с id={data["park_id"]} не существует'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if (car is None):
            response = {
                'car_number': f'Машина с номером {data["car_number"]} не зарегистрирована в базе'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        infos = [i for i in ParkingInfo.objects.filter(
            car=car, checkout_time=None)]
        if (len(infos) > 0):
            response = {
                'car_number': f'Машина с номером {data["car_number"]} уже находится на парковке'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        info = ParkingInfo(park=park, car=car)
        info.save()
        serializer = ParkingInfoSerializer(info)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
