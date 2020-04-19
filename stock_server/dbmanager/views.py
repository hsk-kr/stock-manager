from rest_framework import viewsets

from .models import Stock
from .serializers import StockSerializer


class StockViewset(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
