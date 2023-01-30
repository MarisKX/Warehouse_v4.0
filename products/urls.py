from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('view_product/<code>/', views.product_details, name='product_details'),
    path('add_product/', views.add_product, name='add_product'),
    path('stock_level/', views.stock_level, name='stock_level'),
    path('stock_level/<registration_number>/', views.stock_level_company_level, name='stock_level_company_level'),
    path('stock_level_details/<id>/', views.stock_level_warehouse_level, name='stock_level_warehouse_level'),
]
