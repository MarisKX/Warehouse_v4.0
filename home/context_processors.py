from companies.models import Company
from django.shortcuts import get_object_or_404


def extras(request):
    company = get_object_or_404(Company, owner=request.user)
    all_companies_with_stock = Company.objects.filter(warehouse=True)
    return {
        'company': company,
        'all_companies_with_stock': all_companies_with_stock
    }
