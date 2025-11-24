from django.db import models
from core.models.company import CompanyBaseModel
from inventory.models.category import Category
from inventory.models.units import Unit


class ProductFiscalData(CompanyBaseModel):
    """
    Modelo para representar dados fiscais de produtos.
    """

    ncm = models.CharField(max_length=8, verbose_name="NCM")
    cest = models.CharField(max_length=7, blank=True, null=True, verbose_name="CEST")
    cfop = models.CharField(max_length=4, verbose_name="CFOP Padrão")

    origin = models.CharField(
        max_length=1,
        choices=[
            ('0', 'Nacional'),
            ('1', 'Estrangeira - Importação direta'),
            ('2', 'Estrangeira - Mercado interno'),
        ],
        default='0',
        verbose_name="Origem da Mercadoria"
    )

    cst_icms = models.CharField(max_length=3, blank=True, null=True, verbose_name="CST ICMS")
    cst_pis = models.CharField(max_length=3, blank=True, null=True, verbose_name="CST PIS")
    cst_cofins = models.CharField(max_length=3, blank=True, null=True, verbose_name="CST COFINS")

    icms_aliquota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Alíquota ICMS")
    pis_aliquota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Alíquota PIS")
    cofins_aliquota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Alíquota COFINS")

    class Meta:
        verbose_name = "Dados Fiscais do Produto"
        verbose_name_plural = "Dados Fiscais do Produto"


class Product(CompanyBaseModel):
    """
    Modelo para representar produtos no inventário.
    """

    name = models.CharField(max_length=200, verbose_name='Nome do Produto')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição do Produto')
    
    # Comercial
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    sku = models.CharField(max_length=50, blank=True, null=True, verbose_name='SKU')
    barcode = models.CharField(max_length=20, blank=True, null=True, verbose_name='Código de Barras')

    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Preço de Custo')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço de Venda')

    # Estoque (inicial)
    stock_quantity = models.IntegerField(default=0, verbose_name='Quantidade em Estoque')

    # Fiscal
    fiscal_data = models.OneToOneField(
        ProductFiscalData,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['name']

    def __str__(self):
        return self.name
