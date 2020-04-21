from rest_framework import viewsets

from .models import Stock, CrawlerActivity, Worker
from .serializers import StockSerializer, CrawlerActivitySerializer, WorkerSerializer
from rest_framework import mixins


class StockViewset(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class CrawlerActivityViewSet(viewsets.ModelViewSet):
    serializer_class = CrawlerActivitySerializer
    queryset = CrawlerActivity.objects.all()


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
