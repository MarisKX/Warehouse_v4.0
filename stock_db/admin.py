from django.contrib import admin
from .models import StockItem, StockHistoryEntry

# Register your models here.


class StockHistoryEntryAdmin(admin.TabularInline):
    model = StockHistoryEntry


class StockItemAdmin(admin.ModelAdmin):
    inlines = (StockHistoryEntryAdmin, )
    list_display = (
        'warehouse',
        'product',
        'quantity',
        'price',
        'value',
    )

    ordering = ('warehouse', 'product')


admin.site.register(StockItem, StockItemAdmin)