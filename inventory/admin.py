from django.contrib import admin
from inventory.models import Product, ProductFiscalData, Category, Unit


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'sku', 'barcode', 'cost_price', 'sale_price', 'stock_quantity')
    search_fields = ('name', 'sku', 'barcode')
    list_filter = ('category', 'unit')

@admin.register(ProductFiscalData)
class ProductFiscalDataAdmin(admin.ModelAdmin):
    list_display = ('ncm', 'cest', 'cfop', 'origin', 'cst_icms', 'cst_pis', 'cst_cofins', 'icms_aliquota', 'pis_aliquota', 'cofins_aliquota')
    search_fields = ('ncm', 'cest', 'cfop')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')