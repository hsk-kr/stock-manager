from rest_framework import viewsets

from .models import Stock, CrawlerActivity, Worker, AnalyzedData
from .serializers import (
    StockSerializer,
    CrawlerActivitySerializer,
    WorkerSerializer,
    AnalyzedDataSerializer,
)


class StockViewset(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class CrawlerActivityViewSet(viewsets.ModelViewSet):
    serializer_class = CrawlerActivitySerializer
    queryset = CrawlerActivity.objects.all()


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()


class AnalyzedDataViewSet(viewsets.ModelViewSet):
    serializer_class = AnalyzedDataSerializer
    queryset = AnalyzedData.objects.all()
