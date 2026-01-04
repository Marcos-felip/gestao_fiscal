from django import forms
from inventory.models.product import Product, ProductFiscalData
from inventory.models.category import Category
from inventory.models.units import Unit
from partners.models.suppliers import Supplier


class ProductDataForm(forms.ModelForm):
    """Formulário com informações básicas do produto"""

    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'unit',
            'supplier',
            'sku',
            'barcode',
            'cost_price',
            'sale_price',
            'stock_quantity',
            'description',
        ]
        labels = {
            'name': 'Nome do Produto',
            'description': 'Descrição do Produto',
            'category': 'Categoria',
            'unit': 'Unidade de Medida',
            'supplier': 'Fornecedor',
            'sku': 'Cód. de Referência/SKU',
            'barcode': 'Código de Barras',
            'cost_price': 'Preço de Custo',
            'sale_price': 'Preço de Venda',
            'stock_quantity': 'Quantidade em Estoque',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

        if self.company:
            self.fields['category'].queryset = Category.objects.filter(
                company=self.company,
                is_active=True
            ).order_by('name')
            self.fields['unit'].queryset = Unit.objects.filter(
                company=self.company,
                is_active=True
            ).order_by('name')
            self.fields['supplier'].queryset = Supplier.objects.filter(
                company=self.company,
                is_active=True
            ).order_by('name')

    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price')
        if sale_price and sale_price <= 0:
            raise forms.ValidationError('O preço de venda deve ser maior que zero.')
        return sale_price

    def clean_cost_price(self):
        cost_price = self.cleaned_data.get('cost_price')
        if cost_price and cost_price < 0:
            raise forms.ValidationError('O preço de custo não pode ser negativo.')
        return cost_price

    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity and stock_quantity < 0:
            raise forms.ValidationError('A quantidade em estoque não pode ser negativa.')
        return stock_quantity


class ProductTaxForm(forms.ModelForm):
    """Formulário com dados fiscais do produto"""

    class Meta:
        model = ProductFiscalData
        fields = [
            'ncm',
            'cest',
            'cfop',
            'origin',
            'cst_icms',
            'cst_pis',
            'cst_cofins',
            'icms_aliquota',
            'pis_aliquota',
            'cofins_aliquota',
        ]
        widgets = {
            'ncm': forms.TextInput(attrs={'class': 'form-control'}),
            'cest': forms.TextInput(attrs={'class': 'form-control'}),
            'cfop': forms.TextInput(attrs={'class': 'form-control'}),
            'cst_icms': forms.TextInput(attrs={'class': 'form-control'}),
            'cst_pis': forms.TextInput(attrs={'class': 'form-control'}),
            'cst_cofins': forms.TextInput(attrs={'class': 'form-control'}),
            'icms_aliquota': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pis_aliquota': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cofins_aliquota': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

    def clean_ncm(self):
        ncm = self.cleaned_data.get('ncm')
        if ncm:
            ncm = ''.join(filter(str.isdigit, ncm))
            if len(ncm) != 8:
                raise forms.ValidationError('NCM deve conter 8 dígitos.')
        return ncm

    def clean_cest(self):
        cest = self.cleaned_data.get('cest')
        if cest:
            cest = ''.join(filter(str.isdigit, cest))
            if len(cest) != 7:
                raise forms.ValidationError('CEST deve conter 7 dígitos.')
        return cest

    def clean_cfop(self):
        cfop = self.cleaned_data.get('cfop')
        if cfop:
            cfop = ''.join(filter(str.isdigit, cfop))
            if len(cfop) != 4:
                raise forms.ValidationError('CFOP deve conter 4 dígitos.')
        return cfop