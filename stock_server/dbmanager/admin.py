from django.contrib import admin
from .models import Stock, CrawlerActivity

admin.site.register(Stock)
admin.site.register(CrawlerActivity)
