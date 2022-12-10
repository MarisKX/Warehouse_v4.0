from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db.models import Sum


# Create your models here.
class Company(models.Model):

    class Meta:
        verbose_name_plural = 'Companies'

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=254, blank=True, null=True)
    full_name = models.CharField(max_length=254, blank=True)
    registration_number = models.PositiveIntegerField(blank=True, primary_key=True, default=1)
    invoice_prefix = models.CharField(max_length=2, blank=False, unique=True)
    street_adress_1 = models.IntegerField(default=0, blank=True)
    street_adress_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=6, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.full_name

    def get_house_number(self):
        return self.street_adress_1

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the company name
        if it hasn't been set already.
        """
        if self.registration_number == 1:
            company_count = Company.objects.all().count()
            self.registration_number = f"475010" + str(company_count + 1).zfill(4)
            self.name = self.full_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)


class Warehouse(models.Model):
    warehouse_owner = models.ForeignKey(Company, null=True, blank=False, on_delete=models.CASCADE, related_name='warehouse_owner')
    name = models.CharField(max_length=254, blank=True, null=True)
    full_name = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the warehouse name
        if it hasn't been set already.
        """
        self.name = self.full_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)
