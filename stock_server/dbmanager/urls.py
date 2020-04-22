from django.urls import include, path
from rest_framework import routers

from .views import (
    StockViewset,
    CrawlerActivityViewSet,
    WorkerViewSet,
    AnalyzedDataViewSet,
)

api_router = routers.SimpleRouter()
api_router.register(r"stock", StockViewset)
api_router.register(r"crawleractivity", CrawlerActivityViewSet)
api_router.register(r"worker", WorkerViewSet)
api_router.register(r"analyzeddata", AnalyzedDataViewSet)

urlpatterns = [path("", include(api_router.urls))]
