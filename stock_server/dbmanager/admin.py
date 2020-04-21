from django.contrib import admin
from .models import Stock, CrawlerActivity, Worker
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

    def detail_url(self, obj):
        return format_html(
            "<a href={url} target='_blank'>OPEN</a>", url=obj.stock_detail_link
        )

    detail_url.short_description = "url"


class CrawlerActivityAdmin(admin.ModelAdmin):
    list_display = ("_worker_id", "activity", "created_at")

    def _worker_id(self, obj):
        return obj.worker_id.id


admin.site.register(Stock, StockAdmin)
admin.site.register(CrawlerActivity, CrawlerActivityAdmin)
admin.site.register(Worker, WorkerAdmin)
