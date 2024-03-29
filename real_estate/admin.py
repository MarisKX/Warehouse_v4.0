from django.contrib import admin
from .models import RealEstate, RealEstateCoordinates, RealEstateTypes

# Register your models here.


class RealEstateTypesAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = (
        'name',
        'display_name',
        'color',
    )

    ordering = ('display_name',)


class RealEstateCoordinatesAdmin(admin.TabularInline):
    model = RealEstateCoordinates
    readonly_fields = ()
    list_display = (
        'coordinates_min_E',
        'coordinates_min_S',
        'coordinates_max_E',
        'coordinates_max_S',
        'width',
        'height',
        'field_size_element',
    )

    ordering = ('coordinates_min_E',)


class RealEstateAdmin(admin.ModelAdmin):
    inlines = (RealEstateCoordinatesAdmin, )
    readonly_fields = ('cadastre_number', )
    list_display = (
        'owner_com',
        'owner_pp',
        'property_type',
        'street_adress_1',
        'street_adress_2',
        'city',
        'post_code',
        'country',
        'field_size',
    )

    ordering = ('owner_com', 'owner_pp')


admin.site.register(RealEstate, RealEstateAdmin)
admin.site.register(RealEstateTypes, RealEstateTypesAdmin)