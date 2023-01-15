from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from companies.models import Company

# Create your views here.
@login_required
def index(request):
    """ A view to return the index page """
    owner = request.user
    company = get_object_or_404(Company, owner=owner)
    all_companies_with_stock = Company.objects.filter(warehouse=True)

    context = {
        'company': company,
        'owner': owner,
        'all_companies_with_stock': all_companies_with_stock
    }

    return render(request, 'home/index.html', context)
