from django.urls import include, path
from rest_framework import routers

from .views import (
    StockViewset,
    CrawlerActivityViewSet,
    WorkerViewSet,
    AnalyzedDataViewSet,
    NotAnalyzedDataViewSet,
    CrawlerView,
    AnalyzerView
)

api_router = routers.SimpleRouter()
api_router.register(r"stock", StockViewset)
api_router.register(r"crawleractivity", CrawlerActivityViewSet)
api_router.register(r"worker", WorkerViewSet)
api_router.register(r"analyzeddata", AnalyzedDataViewSet)
api_router.register(r"notanalyzeddata", NotAnalyzedDataViewSet)

urlpatterns = [path("", include(api_router.urls)),
               path("crawler", CrawlerView.as_view()), path("analyzer", AnalyzerView.as_view())]
