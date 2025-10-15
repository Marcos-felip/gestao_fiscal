from django.db import models
from core.models.partners import PartnerBaseModel


class Supplier(PartnerBaseModel):
    """Fornecedor - parceiro que vende produtos/serviços"""
    bank_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Banco')
    bank_agency = models.CharField(max_length=10, blank=True, null=True, verbose_name='Agência')
    bank_account = models.CharField(max_length=20, blank=True, null=True, verbose_name='Conta')
    bank_pix = models.CharField(max_length=100, blank=True, null=True, verbose_name='Chave PIX')
    payment_terms = models.CharField(max_length=255, blank=True, null=True, verbose_name='Condições de Pagamento')
    
    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['name']
        indexes = [
            models.Index(fields=['cpf_cnpj']),
            models.Index(
                fields=[
                    'company',
                    'name'
                ]
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'company',
                    'cpf_cnpj'
                ],
                name='unique_supplier_cpf_cnpj_per_company'
            )
        ]