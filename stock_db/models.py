from django.db import models
from companies.models import Company, Warehouse
from products.models import Product
from django.db.models import Sum

# Create your models here.


class StockItem(models.Model):

    class Meta:
        verbose_name_plural = 'Stock Movements'

    warehouse = models.ForeignKey(
        Warehouse, null=False, blank=False,
        on_delete=models.CASCADE, related_name='item_location')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00, blank=False)
    value = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.value = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name

    def update_saldo(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.quantity = self.element.aggregate(Sum('saldo'))['saldo__sum'] or 0
        self.save()


class StockHistoryEntry(models.Model):
    element = models.ForeignKey(
        'StockItem', null=False, blank=False,
        on_delete=models.CASCADE, related_name='element')
    doc_nr = models.CharField(max_length=254, blank=True, null=True)
    quantity_plus = models.IntegerField(null=True, blank=True, default=0)
    quantity_minus = models.IntegerField(null=True, blank=True, default=0)
    saldo = models.IntegerField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.saldo = self.quantity_plus - self.quantity_minus
        super().save(*args, **kwargs)
