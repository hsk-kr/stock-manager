from django.urls import include, path
from rest_framework import routers

from .views import StockViewset, CrawlerActivityViewSet, WorkerViewSet

api_router = routers.SimpleRouter()
api_router.register(r"stock", StockViewset)
api_router.register(r"crawleractivity", CrawlerActivityViewSet)
api_router.register(r"worker", WorkerViewSet)

urlpatterns = [path("", include(api_router.urls))]
