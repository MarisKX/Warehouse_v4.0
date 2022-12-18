from django.contrib import admin
from .models import Citizen

# Register your models here.

class CitizenAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'bsn_number')
    list_display = (
        'full_name',
        'bsn_number',
    )

    ordering = ('bsn_number',)


admin.site.register(Citizen, CitizenAdmin)