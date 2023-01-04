from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParkViewSet, ParkingInfoViewSet, ParkingRecord, ParkCreate, CarViewSet, PriceViewSet


router = DefaultRouter()
router.register(r'parks', ParkViewSet, basename="parks")
router.register('parkings', ParkingInfoViewSet, basename="parking-infos")
router.register(r'cars', CarViewSet, basename="cars")
router.register('price', PriceViewSet, basename="price")

urlpatterns = [    
    path('parkings/create/', ParkingRecord.as_view()),
    path('parks/create/', ParkCreate.as_view()),
    path('', include(router.urls)),
]
