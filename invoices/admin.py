from django.contrib import admin
from .models import (
    Invoice,
    InvoiceItem,
    WorkOrder,
    WorkOrderItemRawMat,
    WorkOrderItemProduction,
    RetailSale,
    RetailSaleItem,
    ConstructionInvoice,
    ConstructionInvoiceItem,
    ConstructionInvoiceLabourCosts,
)

# Register your models here.


class InvoiceItemAdmin(admin.TabularInline):
    model = InvoiceItem
    readonly_fields = ('lineitem_total', 'btw', 'lineitem_total_with_btw',)


class InvoiceAdmin(admin.ModelAdmin):
    inlines = (InvoiceItemAdmin,)
    readonly_fields = ('amount_total', 'btw_total', 'amount_total_with_btw',)
    list_display = (
        'invoice_number',
        'suplier',
        'customer',
        'date',
        'payment_term',
        'invoice_paid',
        'invoice_paid_confirmed',
        'amount_total',
        'btw_total',
        'amount_total_with_btw', 
    )
    ordering = ('date', 'id',)


class WorkOrderItemRawMatAdmin(admin.TabularInline):
    model = WorkOrderItemRawMat
    list_display = (
        'product',
        'quantity',
    )


class WorkOrderItemProductionAdmin(admin.TabularInline):
    model = WorkOrderItemProduction
    list_display = (
        'product',
        'quantity',
    )


class WorkOrderAdmin(admin.ModelAdmin):
    inlines = (WorkOrderItemRawMatAdmin, WorkOrderItemProductionAdmin, )
    readonly_fields = (
        'work_order_number',
        'enviroment_tax_on_workorder_total',
    )
    list_display = (
        'work_order_number',
        'company',
        'warehouse_raw_materials',
        'warehouse_production',
        'date',
        'enviroment_tax_on_workorder_total',
    )
    ordering = ('date', 'work_order_number',)


class RetailSaleItemAdmin(admin.TabularInline):
    model = RetailSaleItem
    readonly_fields = ('retailitem_total', 'btw', 'retailitem_total_with_btw',)


class RetailSaleAdmin(admin.ModelAdmin):
    inlines = (RetailSaleItemAdmin,)
    readonly_fields = ('retail_sale_number', 'amount_total', 'btw_total', 'amount_total_with_btw',)
    list_display = (
        'retail_sale_number',
        'retailer',
        'customer_city',
        'date',
        'amount_total',
        'btw_total',
        'amount_total_with_btw', 
    )
    ordering = ('date', 'retail_sale_number',)


class ConstructionInvoiceItemAdmin(admin.TabularInline):
    model = ConstructionInvoiceItem
    readonly_fields = ('constructionitem_total', 'btw', 'constructionitem_total_with_btw',)


class ConstructionInvoiceLabourCostsAdmin(admin.TabularInline):
    model = ConstructionInvoiceLabourCosts
    readonly_fields = ('construction_labour_item_total', 'btw', 'construction_labour_item_total_with_btw',)


class ConstructionInvoiceAdmin(admin.ModelAdmin):
    inlines = (ConstructionInvoiceItemAdmin, ConstructionInvoiceLabourCostsAdmin,)
    readonly_fields = ('amount_total', 'btw_total', 'amount_total_with_btw',)
    list_display = (
        'c_invoice_number',
        'constructor',
        'build_customer',
        'date',
        'payment_term',
        'c_invoice_paid',
        'c_invoice_paid_confirmed',
        'amount_total',
        'btw_total',
        'amount_total_with_btw', 
    )
    ordering = ('date', 'c_invoice_number',)


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(RetailSale, RetailSaleAdmin)
admin.site.register(ConstructionInvoice, ConstructionInvoiceAdmin)