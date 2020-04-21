from rest_framework import serializers
from .models import Stock, CrawlerActivity, Worker


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class CrawlerActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlerActivity
        fields = "__all__"


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"
