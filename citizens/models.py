from django.db import models


# Create your models here.
class Citizen(models.Model):

    class Meta:
        verbose_name_plural = 'Citizens'

    name = models.CharField(max_length=254, blank=True, null=True)
    full_name = models.CharField(max_length=254, blank=True)
    bsn_number = models.PositiveIntegerField(blank=True, primary_key=True, default=1)
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
        if self.bsn_number == 1:
            citizen_count = Citizen.objects.all().count()
            self.bsn_number = f"19" + str(citizen_count + 1).zfill(5)
            self.name = self.full_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)