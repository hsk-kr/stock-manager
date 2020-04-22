from django.utils import timezone

from django.db import models
from django.contrib.postgres.fields import JSONField


class Worker(models.Model):
    created_at = models.DateTimeField(default=timezone.now)


class Stock(models.Model):
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=20)
    stock_type = models.CharField(max_length=10)
    stock_detail_link = models.CharField(max_length=256)
    current_stock_price = models.FloatField()
    day_increase = models.FloatField()
    fluctuation = models.FloatField()
    bid = models.FloatField()
    ask = models.FloatField()
    amount_buying = models.FloatField()
    amount_selling = models.FloatField()
    per = models.FloatField()
    roe = models.FloatField()
    continuous_stock_list = JSONField()
    validation_result = models.BooleanField()
    validation_message = models.CharField(max_length=256)
    created_at = models.DateTimeField(default=timezone.now)


class CrawlerActivity(models.Model):
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE)
    activity = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


class AnalyzedData(models.Model):
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    continuous_days = models.IntegerField()
    last_fluctuation = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
