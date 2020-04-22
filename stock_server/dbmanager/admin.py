from django.contrib import admin
from .models import Stock, CrawlerActivity, Worker, AnalyzedData
from django.utils.html import format_html


class WorkerAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")


class StockAdmin(admin.ModelAdmin):
    list_display = (
        "_worker_id",
        "name",
        "detail_url",
        "code",
        "stock_type",
        "current_stock_price",
        "day_increase",
        "fluctuation",
        "validation_result",
        "validation_message",
        "created_at",
    )

    def _worker_id(self, obj):
        return obj.worker_id.id

    _worker_id.short_description = "worker_id"

    def detail_url(self, obj):
        return format_html(
            "<a href={url} target='_blank'>OPEN</a>", url=obj.stock_detail_link
        )

    detail_url.short_description = "url"


class CrawlerActivityAdmin(admin.ModelAdmin):
    list_display = ("_worker_id", "activity", "created_at")

    def _worker_id(self, obj):
        return obj.worker_id.id

    _worker_id.short_description = "worker_id"


class AnalyzedDataAdmin(admin.ModelAdmin):
    list_display = (
        "worker_id",
        "worker_created_at",
        "stock_name",
        "stock_code",
        "stock_detail_url",
        "stock_type",
        "stock_price",
        "continuous_days",
        "last_fluctuation",
        "created_at",
    )

    def worker_id(self, obj):
        return obj.stock_id.worker_id.id

    worker_id.short_description = "worker_id"

    def worker_created_at(self, obj):
        return obj.stock_id.worker_id.created_at

    worker_created_at.short_description = "worker_created_at"

    def stock_name(self, obj):
        return obj.stock_id.name

    stock_name.short_description = "stock_name"

    def stock_code(self, obj):
        return obj.stock_id.code

    stock_code.short_description = "stock_code"

    def stock_detail_url(self, obj):
        return obj.stock_id.stock_detail_link

    stock_detail_url.short_description = "stock_url"

    def stock_type(self, obj):
        return obj.stock_id.stock_type

    stock_type.short_description = "stock_type"

    def stock_price(self, obj):
        return obj.stock_id.current_stock_price

    stock_price.short_description = "stock_price"


admin.site.register(Stock, StockAdmin)
admin.site.register(CrawlerActivity, CrawlerActivityAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(AnalyzedData, AnalyzedDataAdmin)
