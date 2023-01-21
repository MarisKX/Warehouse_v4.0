from django.shortcuts import render, get_object_or_404, reverse
from .models import Product, Category, SubCategory
from companies.models import Company, Warehouse
from stock_db.models import StockItem
from django.http import JsonResponse, HttpResponseRedirect
from .forms import ProductForm, CategoryForm, SubCategoryForm
from django.db.models import Q


# All Products view
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
    }

    return render(request, 'products/products.html', context)


def product_details(request, code):
    """ A view to return the product detail page """

    product = get_object_or_404(Product, code=code)

    context = {
        'product': product,
    }

    return render(request, 'products/product_details.html', context)


# Add New Product view
def add_product(request):
    """ A view to return the product detail page """

    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    all_categories = Category.objects.all()

    if is_ajax(request):
        category = request.GET.get('category')
        if category is not None:
            subcategories = SubCategory.objects.filter(category=category).values_list('display_name')
            subcategories_id = SubCategory.objects.filter(category=category).values_list('id')
            print(subcategories_id, subcategories)
            return JsonResponse({
                "subcategories_to_return": list(subcategories),
                "subcategories_id_to_return": list(subcategories_id),
                })

    add_cat_form = CategoryForm()
    add_subcat_form = SubCategoryForm()
    add_product_form = ProductForm()
    name_field = add_product_form.fields['name']
    name_field.widget = name_field.hidden_widget()
    code_field = add_product_form.fields['code']
    code_field.widget = code_field.hidden_widget()

    if request.method == "POST":
        if 'add-category-btn' in request.POST:
            add_cat_form = CategoryForm(request.POST or None)
            if add_cat_form.is_valid():
                obj = add_cat_form.save(commit=False)
                print(obj)
                obj.save()
                add_cat_form = CategoryForm()
                return HttpResponseRedirect(reverse("add_product"))
        elif 'add-subcategory-btn' in request.POST:
            add_subcat_form = SubCategoryForm(request.POST or None)
            if add_subcat_form.is_valid():
                obj = add_subcat_form.save(commit=False)
                obj.save()
                add_subcat_form = SubCategoryForm()
        elif 'add-product-btn' in request.POST:
            add_product_form = ProductForm(request.POST or None, request.FILES)
            if add_product_form.is_valid():
                obj = add_product_form.save(commit=False)
                obj.save()
                add_product_form = ProductForm()
                name_field = add_product_form.fields['name']
                name_field.widget = name_field.hidden_widget()
                code_field = add_product_form.fields['code']
                code_field.widget = code_field.hidden_widget()

    context = {
        'all_categories': all_categories,
        'add_category': add_cat_form,
        'add_subcategory': add_subcat_form,
        'add_product': add_product_form,
    }

    return render(request, 'products/add_product.html', context)


# Edit Product view (coming soon)

# Stock Level view
def stock_level(request):
    """ A view to return the product detail page """

    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    stock_items = StockItem.objects.all().order_by('warehouse')
    print(stock_items)

    context = {
        'stock_items': stock_items,
    }

    return render(request, 'products/stock_level.html', context)


# Stock Level view for company
def stock_level_company_level(request, registration_number):
    """ A view to return the product detail page """

    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    company_to_display = get_object_or_404(Company, registration_number=registration_number)
    queries = Q(warehouse__name__icontains=company_to_display)

    stock_items = StockItem.objects.filter(queries)

    context = {
        'company_to_display': company_to_display,
        'stock_items': stock_items
    }

    return render(request, 'products/stock_level_company_level.html', context)
