from django.urls import include, path
from rest_framework import routers

from .views import StockViewset, CrawlerActivityViewSet

api_router = routers.SimpleRouter()
api_router.register(r'stock', StockViewset)
api_router.register(r'crawleractivity', CrawlerActivityViewSet)

urlpatterns = [
    path('', include(api_router.urls))
]
