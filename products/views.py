from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from companies.models import Company, Warehouse
from stock_db.models import StockItem
from django.http import JsonResponse


# Create your views here.
def all_products(request):
    """ A view to show all products, including sorting and search queries """

    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    products = Product.objects.all().order_by("full_name")
    all_categories = Category.objects.all()
    all_warehouses = Warehouse.objects.all()
    all_stock_items = StockItem.objects.all()
    all_companies = Company.objects.all()

    categories = None
    company = get_object_or_404(Company, owner=request.user)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if is_ajax(request):
        product_code = request.GET.get('product')
        product = get_object_or_404(Product, code=product_code)
        warehouse_list = StockItem.objects.filter(product=product).values_list('warehouse__full_name')
        stock_list = StockItem.objects.filter(product=product).values_list('quantity')
        price_list = StockItem.objects.filter(product=product).values_list('price')
        return JsonResponse({
            "warehouses_to_return": list(warehouse_list),
            "stock_to_return": list(stock_list),
            "price_to_return": list(price_list)
            })

    context = {
        'products': products,
        'all_categories': all_categories,
        'all_warehouses': all_warehouses,
        'all_stock_items': all_stock_items,
        'company': company,
    }

    return render(request, 'products/products.html', context)


def product_details(request, code):
    """ A view to return the product detail page """

    product = get_object_or_404(Product, code=code)
    company = get_object_or_404(Company, owner=request.user)

    context = {
        'product': product,
        'company': company,
    }

    return render(request, 'products/product_details.html', context)
