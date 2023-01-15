from django.contrib import admin
from .models import Company, Warehouse, Employees

# Register your models here.


class WarehouseAdmin(admin.TabularInline):
    model = Warehouse
    readonly_fields = ('name', )
    list_display = (
        'owner',
        'full_name',
    )

    ordering = ('full_name',)


class EmployeesAdmin(admin.TabularInline):
    model = Employees
    readonly_fields = (
        'salary_vsaoi_dd',
        'salary_vsaoi_dn',
        'salary_iin',
        'salary_netto',
        )
    list_display = (
        'company',
        'name',
        'salary_brutto'
    )

    ordering = ('name',)


class CompanyAdmin(admin.ModelAdmin):
    inlines = (WarehouseAdmin, EmployeesAdmin)
    readonly_fields = ('name', 'total_bruto_salaries', 'total_salary_netto', )
    list_display = (
        'full_name',
        'invoice_prefix',
        'registration_number',
        'warehouse',
        'total_bruto_salaries',
        'total_salary_netto',

    )

    ordering = ('full_name',)


admin.site.register(Company, CompanyAdmin)
