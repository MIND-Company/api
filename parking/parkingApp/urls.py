from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import OwnerParkViewSet, ParkViewSet, ParkingInfoViewSet, ParkingRecordViewSet, ParkCreate, CarViewSet, PriceViewSet, ParkingRecordCheckout
from django.views.generic.base import RedirectView


router = DefaultRouter()
router.register('entry-register', ParkingRecordViewSet, basename="parking-create")
router.register('all-parks', ParkViewSet, basename="all-parks")
router.register('owner-parks', OwnerParkViewSet, basename="owner-parks")
router.register('parkings', ParkingInfoViewSet, basename="parking-infos")
router.register('cars', CarViewSet, basename="cars")
router.register('price', PriceViewSet, basename="price")


urlpatterns = [    
    path('checkout-register/', ParkingRecordCheckout.as_view()),
    path('parks/create/', ParkCreate.as_view()),
    path('', include(router.urls)),
]
