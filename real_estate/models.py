from django.db import models
from companies.models import Company
from citizens.models import Citizen

# Create your models here.


class RealEstateTypes(models.Model):
    name = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Real Estate Types'

    def __str__(self):
        return self.name


class RealEstate(models.Model):

    class Meta:
        verbose_name_plural = 'Real Estate'

    owner_com = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE, related_name='real_estate_owner_com')
    owner_pp = models.ForeignKey(Citizen, null=True, blank=True, on_delete=models.CASCADE, related_name='real_estate_owner_pp')
    property_type = models.ForeignKey(RealEstateTypes, null=False, blank=False, on_delete=models.CASCADE, related_name='real_estate_type')
    cadastre_number = models.CharField(max_length=8, blank=False, primary_key=True, default=1)
    street_adress_1 = models.IntegerField(default=0, blank=True, null=True)
    street_adress_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=6, blank=True)
    country = models.CharField(max_length=100, blank=True)
    field_size = models.IntegerField(default=0, blank=True)
    center_coordinates_min_E = models.IntegerField(default=0, blank=False)
    center_coordinates_min_S = models.IntegerField(default=0, blank=False)
    cadastre_value = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.cadastre_number)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the cadastre number
        if it hasn't been set already.
        """
        if self.cadastre_number == '1':
            property_count = RealEstate.objects.all().count()
            self.cadastre_number = self.city[0:3].upper() + str(property_count + 1).zfill(5)
        super().save(*args, **kwargs)


class RealEstateCoordinates(models.Model):
    real_estate = models.ForeignKey(RealEstate, null=True, blank=False, on_delete=models.CASCADE, related_name='real_estate')
    coordinates_min_E = models.IntegerField(default=0, blank=False)
    coordinates_min_S = models.IntegerField(default=0, blank=False)
    coordinates_max_E = models.IntegerField(default=0, blank=False)
    coordinates_max_S = models.IntegerField(default=0, blank=False)
    width = models.IntegerField(default=0, blank=False)
    height = models.IntegerField(default=0, blank=False)
    field_size_element = models.IntegerField(default=0, blank=True)
