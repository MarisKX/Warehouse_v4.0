from django.db import models
from django.db.models import Sum
from citizens.models import Citizen
from companies.models import Company, Warehouse
from invoices.models import Invoice, WorkOrder, RetailSale, ConstructionInvoice


# Create your models here.
class Report(models.Model):

    class Meta:
        verbose_name_plural = 'Reports'

    date = models.DateField(auto_now_add=False)
    report_type_choices = [
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    ]
    report_type = models.CharField(max_length=16, choices=report_type_choices, default='M')
    month_choices = [
        (1, "January"), (2, "February"), (3, "March"),
        (4, "April"), (5, "May"), (6, "June"),
        (7, "July"), (8, "August"), (9, "September"),
        (10, "October"), (11, "November"), (12, "December"),
        ]
    report_year = models.IntegerField()
    report_month = models.IntegerField(choices=month_choices)
    report_number = models.CharField(max_length=10, default=1, primary_key=True)
    gpd_from_invoices = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gpd_from_retail = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gpd_from_construction = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gpd_in_period = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.report_number

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the company name
        if it hasn't been set already.
        """
        if self.report_number == 1:
            if self.report_type == "M":
                report_count = Report.objects.filter(report_type='M').count()
                self.report_number = f"REP-MO-" + str(report_count + 1).zfill(5)
            else:
                report_count = Report.objects.filter(report_type='Y').count()
                self.report_number = f"REP-YE-" + str(report_count + 1).zfill(5)

            all_sales = Invoice.objects.filter(date__year=self.report_year, date__month=self.report_month)
            invoice_gpd_dic = all_sales.aggregate(Sum('amount_total'))
            self.gpd_from_invoices = invoice_gpd_dic['amount_total__sum']

            all_retail_sales = RetailSale.objects.filter(date__year=self.report_year, date__month=self.report_month)
            retail_gpd_dic = all_retail_sales.aggregate(Sum('amount_total'))
            self.gpd_from_retail = retail_gpd_dic['amount_total__sum']

            all_construction = ConstructionInvoice.objects.filter(date__year=self.report_year, date__month=self.report_month)
            construction_gpd_dic = all_construction.aggregate(Sum('amount_total'))
            self.gpd_from_construction = construction_gpd_dic['amount_total__sum']

            self.gpd_in_period = self.gpd_from_invoices + self.gpd_from_retail + self.gpd_from_construction

        super().save(*args, **kwargs)