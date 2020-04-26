from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

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
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("worker_id__id", "validation_result")


class CrawlerActivityViewSet(viewsets.ModelViewSet):
    serializer_class = CrawlerActivitySerializer
    queryset = CrawlerActivity.objects.all()


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()


class AnalyzedDataViewSet(viewsets.ModelViewSet):
    serializer_class = AnalyzedDataSerializer
    queryset = AnalyzedData.objects.all()
