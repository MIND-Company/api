from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import ParkSerializer
from .models import Park


class ParkViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        user = self.request.user
        if not user.id:
            return []
        return Park.objects.filter(owner=user)

    serializer_class = ParkSerializer
    permission_classes = [permissions.IsAuthenticated]
