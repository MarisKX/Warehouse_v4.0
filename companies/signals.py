from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Warehouse, Company, Employees
from stock_db.models import StockHistoryEntry, StockItem
from invoices.models import (
    InvoiceItem,
    WorkOrderItemRawMat,
    WorkOrderItemProduction,
    RetailSaleItem,
    ConstructionInvoice,
    ConstructionInvoiceItem,
    TransferOrder,
    TransferOrderItem
)


@receiver(post_save, sender=StockHistoryEntry)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.element.update_saldo()


@receiver(post_delete, sender=StockHistoryEntry)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.element.update_saldo()


@receiver(post_save, sender=InvoiceItem)
def create_stockmovement_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    if created:
        suplier_warehouse = get_object_or_404(
            Warehouse, warehouse_owner=instance.invoice.suplier_warehouse)
        customer_warehouse = get_object_or_404(
            Warehouse, warehouse_owner=instance.invoice.customer_warehouse)
        try:
            stock_item_suplier = StockItem.objects.get(
                warehouse=suplier_warehouse, product=instance.product)
            stock_item_suplier.price = instance.price
            stock_item_suplier.save()
        except StockItem.DoesNotExist:
            StockItem.objects.create(
                warehouse=suplier_warehouse,
                product=instance.product,
            )
        stock_item_suplier = StockItem.objects.get(
            warehouse=suplier_warehouse, product=instance.product)
        stock_item_suplier.price = instance.price
        stock_item_suplier.save()
        StockHistoryEntry.objects.create(
            element=stock_item_suplier,
            doc_nr=instance.invoice.invoice_number,
            quantity_minus=instance.quantity
        )
        try:
            stock_item_customer = StockItem.objects.get(
                warehouse=customer_warehouse, product=instance.product)
        except StockItem.DoesNotExist:
            StockItem.objects.create(
                warehouse=customer_warehouse,
                product=instance.product,
            )
        stock_item_customer = StockItem.objects.get(
            warehouse=customer_warehouse, product=instance.product)
        StockHistoryEntry.objects.create(
            element=stock_item_customer,
            doc_nr=instance.invoice.invoice_number,
            quantity_plus=instance.quantity
        )


@receiver(post_save, sender=WorkOrderItemRawMat)
def create_raw_mat_stock_movement_on_work_order_save(
        sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    if created:
        raw_warehouse = get_object_or_404(
            Warehouse, name=instance.work_order.warehouse_raw_materials.name)
        try:
            stock_item_raw = StockItem.objects.get(
                warehouse=raw_warehouse, product=instance.product)
        except StockItem.DoesNotExist:
            StockItem.objects.create(
                warehouse=raw_warehouse,
                product=instance.product,
            )
        stock_item_raw = StockItem.objects.get(
            warehouse=raw_warehouse, product=instance.product)
        StockHistoryEntry.objects.create(
            element=stock_item_raw,
            doc_nr=instance.work_order.work_order_number,
            quantity_minus=instance.quantity
        )


@receiver(post_save, sender=WorkOrderItemProduction)
def create_prod_stock_movement_on_work_order_save(
        sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    if created:
        prod_warehouse = get_object_or_404(
            Warehouse, name=instance.work_order.warehouse_production.name)
        try:
            stock_item_prod = StockItem.objects.get(
                warehouse=prod_warehouse, product=instance.product)
        except StockItem.DoesNotExist:
            StockItem.objects.create(
                warehouse=prod_warehouse,
                product=instance.product,
            )
        stock_item_prod = StockItem.objects.get(
            warehouse=prod_warehouse, product=instance.product)
        StockHistoryEntry.objects.create(
            element=stock_item_prod,
            doc_nr=instance.work_order.work_order_number,
            quantity_plus=instance.quantity
        )


@receiver(post_save, sender=TransferOrderItem)
def create_prod_stock_movement_on_transfer_order_save(
        sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    if created:
        warehouse_from = get_object_or_404(
            Warehouse, name=instance.to_number.warehouse_from.name)

        warehouse_to = get_object_or_404(
            Warehouse, name=instance.to_number.warehouse_to.name)

        try:
            warehouse_from_stock_item = StockItem.objects.get(
                warehouse=warehouse_from, product=instance.product)
        except StockItem.DoesNotExist:
            StockItem.objects.create(
                warehouse=warehouse_from_stock_item,
                product=instance.product,
            )
        warehouse_from_stock_item = StockItem.objects.get(
            warehouse=warehouse_from, product=instance.product)
        StockHistoryEntry.objects.create(
            element=warehouse_from_stock_item,
            doc_nr=instance.to_number.to_number,
            quantity_minus=instance.quantity
        )
        try:
            warehouse_to_stock_item = StockItem.objects.get(
                warehouse=warehouse_to, product=instance.product)
        except StockItem.DoesNotExist:
            StockItem.objects.create(
                warehouse=warehouse_to,
                product=instance.product,
            )
        warehouse_to_stock_item = StockItem.objects.get(
            warehouse=warehouse_to, product=instance.product)
        StockHistoryEntry.objects.create(
            element=warehouse_to_stock_item,
            doc_nr=instance.to_number.to_number,
            quantity_plus=instance.quantity
        )


@receiver(post_save, sender=RetailSaleItem)
def create_stockmovement_on_save_for_retail(
        sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    if created:
        retailer_warehouse = get_object_or_404(
            Warehouse, name=instance.retail_sale.retailer_warehouse)
        stock_item_retailer = StockItem.objects.get(
            warehouse=retailer_warehouse, product=instance.product)
        StockHistoryEntry.objects.create(
            element=stock_item_retailer,
            doc_nr=instance.retail_sale.retail_sale_number,
            quantity_minus=instance.quantity
        )


@receiver(post_save, sender=ConstructionInvoiceItem)
def create_stockmovement_on_save_for_contstruction(sender, instance, **kwargs):
    """
    Update order total on lineitem update/create
    """
    if instance.c_invoice.construction_completed is True:
        print("Signal!")
        constructor_warehouse = get_object_or_404(
            Warehouse, name=instance.c_invoice.constructor_warehouse)
        stock_item_constructor = StockItem.objects.get(
            warehouse=constructor_warehouse, product=instance.product)
        StockHistoryEntry.objects.create(
            element=stock_item_constructor,
            doc_nr=instance.c_invoice.c_invoice_number,
            quantity_minus=instance.quantity
        )


@receiver(post_save, sender=Employees)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.company.salaries_total()


@receiver(post_delete, sender=Employees)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.company.salaries_total()
