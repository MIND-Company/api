from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParkViewSet, ParkingInfoViewSet, ParkingRecord, ParkCreate


router = DefaultRouter()
router.register(r'parks', ParkViewSet, basename="parks")
router.register('parkings', ParkingInfoViewSet, basename="parking-infos")

urlpatterns = [
    path('', include(router.urls)),
    path('parkings/create', ParkingRecord.as_view()),
    path('parks/create', ParkCreate.as_view()),
]
