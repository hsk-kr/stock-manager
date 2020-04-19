from django.urls import include, path
from rest_framework import routers

from .views import StockViewset

api_router = routers.SimpleRouter()
api_router.register(r'stock', StockViewset)

urlpatterns = [
    path('', include(api_router.urls))
]
