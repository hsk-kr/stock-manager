import subprocess
from rest_framework import viewsets, mixins, status, filters
from rest_framework.response import Response
from django import forms
from django.views import View
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


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
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['stock_id__worker_id']
    ordering_fields = ['continuous_days', 'last_fluctuation', 'created_at']

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


class CrawlerValidationForm(forms.Form):
    min_daily_increase_per = forms.FloatField()
    avg_trading_volumn = forms.FloatField()
    min_stock_price = forms.FloatField()
    max_stock_price = forms.FloatField()


p_crawler = None  # Global variable used in CrawlerView to execute crawler only one
@method_decorator(csrf_exempt, name="dispatch")
class CrawlerView(View):
    def get(self, request):
        global p_crawler
        if p_crawler != None and p_crawler.poll() == None:
            return JsonResponse({"msg": "already executed wait till ending of the process"}, status=226)
        else:
            return JsonResponse({"msg": "ready to execute"}, status=200)

    def post(self, request):
        form = CrawlerValidationForm(request.POST)

        if not form.is_valid():
            return JsonResponse({"msg": "Bad request"}, status=400)

        global p_crawler

        if p_crawler != None:
            if p_crawler.poll() == None:
                return JsonResponse({"msg": "already executed wait till ending of the process"}, status=226)
            else:
                p_crawler = None
        proc_params = ["python", "../stock_crawler/manager.py"]
        proc_params.extend(["all", request.POST["min_daily_increase_per"], request.POST["avg_trading_volumn"],
                            request.POST["min_stock_price"], request.POST["max_stock_price"]])
        p_crawler = subprocess.Popen(
            proc_params, stdout=subprocess.PIPE)

        return JsonResponse({"msg": "success to execute"}, status=202)


p_analyzer = None
@method_decorator(csrf_exempt, name="dispatch")
class AnalyzerView(View):
    def get(self, request):
        global p_analyzer
        if p_analyzer != None and p_analyzer.poll() == None:
            return JsonResponse({"msg": "already executed wait till ending of the process"}, status=226)
        else:
            return JsonResponse({"msg": "ready to execute"}, status=200)

    def post(self, request):
        global p_analyzer

        if p_analyzer != None:
            if p_analyzer.poll() == None:
                return JsonResponse({"msg": "already executed wait till ending of the process"}, status=226)
            else:
                p_analyzer = None
        proc_params = ["python", "../stock_analyzer/analyzer.py"]
        p_analyzer = subprocess.Popen(
            proc_params, stdout=subprocess.PIPE)

        return JsonResponse({"msg": "success to execute"}, status=202)
