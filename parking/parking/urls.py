from django.contrib import admin
from django.urls import path, include
from parkingAuth import urls as auth_urls
from parkingApp import urls as app_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(auth_urls)),
    path('api/', include(app_urls))
]
