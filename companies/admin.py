from django.contrib import admin
from .models import Company, Warehouse

# Register your models here.


class WarehouseAdmin(admin.TabularInline):
    model = Warehouse
    readonly_fields = ('name', )
    list_display = (
        'owner',
        'full_name',
    )

    ordering = ('full_name',)


class CompanyAdmin(admin.ModelAdmin):
    inlines = (WarehouseAdmin, )
    readonly_fields = ('name',)
    list_display = (
        'full_name',
        'invoice_prefix',
        'registration_number',
    )

    ordering = ('full_name',)


admin.site.register(Company, CompanyAdmin)
