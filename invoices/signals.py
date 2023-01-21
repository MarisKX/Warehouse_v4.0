from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import (
    InvoiceItem,
    Invoice,
    WorkOrder,
    WorkOrderItemProduction,
    WorkOrderItemRawMat,
    RetailSale,
    RetailSaleItem,
    ConstructionInvoice,
    ConstructionInvoiceItem,
    ConstructionInvoiceLabourCosts,
    TransferOrder,
    TransferOrderItem
)


@receiver(post_save, sender=Invoice)
def create_on_save(sender, instance, created, **kwargs):
    """
    Create Invoice number
    """
    if instance.invoice_number == "AA00001":
        invoice_count = Invoice.objects.filter(suplier=instance.suplier).count()
        invoice_prefix = instance.suplier.invoice_prefix
        instance.invoice_number = invoice_prefix + str(invoice_count).zfill(5)
        instance.save()


@receiver(post_save, sender=WorkOrder)
def create_wo_on_save(sender, instance, **kwargs):
    """
    Create Work order number
    """
    if instance.work_order_number == "WO00001":
        workorder_count = WorkOrder.objects.filter(company=instance.company).count()
        invoice_prefix = instance.company.invoice_prefix
        instance.work_order_number = invoice_prefix + "WO" + str(workorder_count).zfill(5)
        instance.save()


@receiver(post_save, sender=TransferOrder)
def create_to_on_save(sender, instance, **kwargs):
    """
    Create Transfer Order number
    """
    if instance.to_number == "TO00001":
        to_count = TransferOrder.objects.filter(company=instance.company).count()
        invoice_prefix = instance.company.invoice_prefix
        instance.to_number = invoice_prefix + "TO" + str(to_count).zfill(5)
        instance.save()


@receiver(post_save, sender=InvoiceItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.invoice.update_invoice_total()


@receiver(post_delete, sender=InvoiceItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.invoice.update_invoice_total()


@receiver(post_save, sender=WorkOrderItemProduction)
def update_on_save_wo_tax(sender, instance, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.work_order.update_tax_wo_total()


@receiver(post_save, sender=RetailSale)
def create_on_save(sender, instance, created, **kwargs):
    """
    Create Invoice number
    """
    if instance.retail_sale_number == "RT1":
        retail_sale_count = RetailSale.objects.filter(retailer=instance.retailer).count()
        invoice_prefix = instance.retailer.invoice_prefix
        instance.retail_sale_number = "RT" + invoice_prefix + str(retail_sale_count).zfill(8)
        instance.save()


@receiver(post_save, sender=RetailSaleItem)
def update_retail_sale_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.retail_sale.update_retail_sale_total()


@receiver(post_save, sender=ConstructionInvoice)
def create_on_save(sender, instance, created, **kwargs):
    """
    Create Invoice number
    """
    if instance.c_invoice_number == "C1":
        c_invoice_count = ConstructionInvoice.objects.filter(constructor=instance.constructor).count()
        invoice_prefix = instance.constructor.invoice_prefix
        instance.c_invoice_number = "CI" + invoice_prefix + str(c_invoice_count).zfill(5)
        instance.save()


@receiver(post_save, sender=ConstructionInvoiceItem)
def update_construction_invoice_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.c_invoice.update_c_invoice_total()


@receiver(post_save, sender=ConstructionInvoiceLabourCosts)
def update_construction_invoice_on_save_labour_costs(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.c_invoice.update_c_invoice_total()
