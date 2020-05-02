from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        """
            It accepts a multiple insertion.
        """
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class NotAnalyzedDataViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
      Returns stocks that not in analyzed_data.
    """
    serializer_class = StockSerializer
    queryset = Stock.objects.filter(analyzeddata__isnull=True)
