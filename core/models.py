from django.db import models


class CompanyBaseModel(models.Model):
    """Base abstrata com controle de Empresa."""
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE, related_name='%(class)ss')
    is_active = models.BooleanField(default=True, verbose_name='Ativo', help_text='Indica se o registro está ativo ou inativo.')

    class Meta:
        abstract = True

__all__ =[
    'CompanyBaseModel',
]