from rest_framework import viewsets

from .models import Stock, CrawlerActivity
from .serializers import StockSerializer, CrawlerActivitySerializer


class StockViewset(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class CrawlerActivityViewSet(viewsets.ModelViewSet):
    serializer_class = CrawlerActivitySerializer
    queryset = CrawlerActivity.objects.all()
