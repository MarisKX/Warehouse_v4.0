from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from companies.models import Company

# Create your views here.
@login_required
def index(request):
    """ A view to return the index page """
    owner = request.user
    company = get_object_or_404(Company, owner=owner)
    
    context = {
        'company': company,
        'owner': owner,
    }
    return render(request, 'home/index.html', context)
