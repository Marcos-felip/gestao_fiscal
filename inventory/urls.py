from django.urls import path
from inventory.views import category, product, unit

app_name = 'inventory'

urlpatterns = [
    path('categories/', category.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', category.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', category.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', category.CategoryDeleteView.as_view(), name='category_delete'),

    path('units/', unit.UnitListView.as_view(), name='unit_list'),
    path('units/create/', unit.UnitCreateView.as_view(), name='unit_create'),
    path('units/<int:pk>/update/', unit.UnitUpdateView.as_view(), name='unit_update'),
    path('units/<int:pk>/delete/', unit.UnitDeleteView.as_view(), name='unit_delete'),

    path('products/create/', product.ProductTemplateView.as_view(), name='product_base'),
    path('products/', product.ProductListView.as_view(), name='product_list'),
    path('products/create/data/', product.ProductDataCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', product.ProductDataUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/tax/', product.ProductTaxUpdateView.as_view(), name='product_tax'),
    path('products/<int:pk>/delete/', product.ProductDeleteView.as_view(), name='product_delete'),
]