from django.db import models
from core.models.partners import PartnerBaseModel


class Customer(PartnerBaseModel):
    """Cliente - parceiro que compra produtos/serviços"""
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Limite de Crédito')
    is_exempt = models.BooleanField(default=False, verbose_name='Isento de Impostos')
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
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
                name='unique_customer_cpf_cnpj_per_company'
            )
        ]