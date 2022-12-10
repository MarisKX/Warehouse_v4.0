from django.db import models
from companies.models import Company
from companies.models import Warehouse


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the category name
        """
        self.name = self.display_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)


class SubCategory(models.Model):

    class Meta:
        verbose_name_plural = 'Subcategories'

    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the subcategory name
        """
        self.name = self.display_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)


class Product(models.Model):

    class Meta:
        ordering = ['name']

    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    subcategory = models.ForeignKey('SubCategory', null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=6, unique=True, default='AA001')
    name = models.CharField(max_length=100, default='name')
    full_name = models.CharField(max_length=100)
    enviroment_tax = models.BooleanField(default=False)
    enviroment_tax_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the subcategory name
        """
        if self.name == 'name':
            self.name = self.full_name.replace(" ", "_").lower()
        if self.code == 'AA001':
            same_cat_products_count = Product.objects.filter(subcategory=self.subcategory).count()
            self.code = (
                self.category.name[0].upper() +
                self.category.name[1].upper() +
                self.subcategory.name[0].upper() +
                self.subcategory.name[1].upper() +
                str(same_cat_products_count + 1).zfill(3)
                )
        super().save(*args, **kwargs)


class ProductPrices(models.Model):

    class Meta:
        verbose_name_plural = 'Product Prices'

    product = models.ForeignKey('Product', null=True, blank=True, on_delete=models.SET_NULL)
    warehouse = models.ForeignKey(Warehouse, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
