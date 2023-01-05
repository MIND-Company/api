from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParkViewSet, ParkingInfoViewSet, ParkingRecordViewSet, ParkCreate, CarViewSet, PriceViewSet, ParkingRecordCheckout


router = DefaultRouter()
router.register('entry-register', ParkingRecordViewSet, basename="parking-create")
router.register('parks', ParkViewSet, basename="parks")
router.register('parkings', ParkingInfoViewSet, basename="parking-infos")
router.register('cars', CarViewSet, basename="cars")
router.register('price', PriceViewSet, basename="price")


urlpatterns = [    
    path('checkout-register/', ParkingRecordCheckout.as_view()),
    path('parks/create/', ParkCreate.as_view()),
    path('', include(router.urls)),
]
