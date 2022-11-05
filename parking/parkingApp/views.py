from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import ParkSerializer, ParkingInfoSerializer
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
