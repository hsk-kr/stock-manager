from rest_framework import serializers
from .models import Stock, CrawlerActivity


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class CrawlerActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlerActivity
        fields = "__all__"
