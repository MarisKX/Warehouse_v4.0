from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from citizens.models import Citizen
from home.models import AppSettings


# Create your models here.
class Company(models.Model):

    class Meta:
        verbose_name_plural = 'Companies'

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=254, blank=True, null=True)
    full_name = models.CharField(max_length=254, blank=True)
    warehouse = models.BooleanField(default=False)
    registration_number = models.PositiveIntegerField(
        blank=True,
        primary_key=True,
        default=1)
    invoice_prefix = models.CharField(max_length=2, blank=False, unique=True)
    street_adress_1 = models.IntegerField(default=0, blank=True)
    street_adress_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=6, blank=True)
    country = models.CharField(max_length=100, blank=True)
    total_bruto_salaries = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_vsaoi_dd = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_vsaoi_dn = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_iin = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_netto = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.full_name

    def get_house_number(self):
        return self.street_adress_1

    def salaries_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.total_bruto_salaries = self.employer.aggregate(
            Sum('salary_brutto'))['salary_brutto__sum'] or 0
        self.total_salary_vsaoi_dd = self.employer.aggregate(
            Sum('salary_vsaoi_dd'))['salary_vsaoi_dd__sum'] or 0
        self.total_salary_vsaoi_dn = self.employer.aggregate(
            Sum('salary_vsaoi_dn'))['salary_vsaoi_dn__sum'] or 0
        self.total_salary_iin = self.employer.aggregate(
            Sum('salary_iin'))['salary_iin__sum'] or 0
        self.total_salary_netto = self.employer.aggregate(
            Sum('salary_netto'))['salary_netto__sum'] or 0
        super().save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the company name
        if it hasn't been set already.
        """
        if self.registration_number == 1:
            company_count = Company.objects.all().count()
            self.registration_number = f"475010" + str(
                company_count + 1).zfill(4)
            self.name = self.full_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)


class Warehouse(models.Model):
    warehouse_owner = models.ForeignKey(
        Company,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='warehouse_owner')
    name = models.CharField(max_length=254, blank=True, null=True)
    full_name = models.CharField(max_length=254, blank=True)
    internal_warehouse = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the warehouse name
        if it hasn't been set already.
        """
        self.name = self.full_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)


class Employees(models.Model):
    company = models.ForeignKey(
        Company,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='employer')
    name = models.ForeignKey(
        Citizen,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='employee')
    role = models.CharField(max_length=254, blank=True, null=True)
    salary_brutto = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    salary_vsaoi_dd = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    salary_vsaoi_dn = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    salary_iin = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    salary_netto = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the salary levels
        if it hasn't been set already.
        """
        latest_settings = get_object_or_404(AppSettings, valid=True)
        self.salary_vsaoi_dd = (self.salary_brutto / 100) * 35
        self.salary_vsaoi_dn = (self.salary_brutto / 100) * 9
        iin_calc = (
            (self.salary_brutto - self.salary_vsaoi_dn - latest_settings.no_iin_level) / 100) * 15
        if iin_calc > 0:
            self.salary_iin = ((
                self.salary_brutto - self.salary_vsaoi_dn - latest_settings.no_iin_level) / 100) * 15
        else:
            self.salary_iin = 0
        self.salary_netto = (
            self.salary_brutto - self.salary_vsaoi_dn - self.salary_iin)
        super().save(*args, **kwargs)
