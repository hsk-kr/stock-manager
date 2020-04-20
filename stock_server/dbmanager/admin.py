from django.contrib import admin
from .models import Stock, CrawlerActivity
from django.utils.html import format_html


class StockAdmin(admin.ModelAdmin):
    list_display = (
        "work_uuid",
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

    def detail_url(self, obj):
        return format_html(
            "<a href={url} target='_blank'>OPEN</a>", url=obj.stock_detail_link
        )

    detail_url.short_description = "url"


class CrawlerActivityAdmin(admin.ModelAdmin):
    list_display = ("work_uuid", "activity", "created_at")


admin.site.register(Stock, StockAdmin)
admin.site.register(CrawlerActivity, CrawlerActivityAdmin)
