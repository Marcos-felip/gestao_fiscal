from django.db import models
import uuid
from django.utils import timezone
from accounts.models.address import Address
from core.models import CompanyBaseModel


class Company(models.Model):
    """Representa a pessoa jurídica (empresa) agregadora de matriz e filiais."""
    class TaxRegime(models.TextChoices):
        SIMPLES = 'simples', 'Simples Nacional'
        SIMPLES_EXCESSO = 'simples_excesso', 'Simples Nacional – Excesso sublimite'
        PRESUMIDO = 'presumido', 'Lucro Presumido'
        REAL = 'real', 'Lucro Real'

    legal_name = models.CharField(max_length=255, verbose_name='Razão Social')
    trade_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nome Fantasia')
    slug = models.SlugField(max_length=255, unique=True)
    key = models.CharField(max_length=50, unique=True, verbose_name='Chave de acesso')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.legal_name}"

class Establishment(CompanyBaseModel):
    """Estabelecimento físico/fiscal (matriz ou filial) emissor de documentos fiscais."""

    class Environment(models.TextChoices):
        PRODUCTION = 'production', 'Production'
        HOMOLOGATION = 'homologation', 'Homologation'

    cnpj = models.CharField(max_length=14, unique=True, verbose_name='CNPJ')
    state_registration = models.CharField(max_length=20, blank=True, verbose_name='Inscrição Estadual')
    municipal_registration = models.CharField(max_length=20, blank=True, verbose_name='Inscrição Municipal')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='establishments', verbose_name='Endereço')
    phone = models.CharField(max_length=15, verbose_name=u'Telefone', null=True, blank=True)
    is_matrix = models.BooleanField(default=False)
    environment_default = models.CharField(max_length=20, choices=Environment.choices, default=Environment.PRODUCTION, verbose_name='Ambiente Padrão')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Estabelecimento'
        verbose_name_plural = 'Estabelecimentos'
        constraints = [
            models.UniqueConstraint(
                fields=['company'],
                condition=models.Q(is_matrix=True),
                name='unique_matrix_per_company'
            )
        ]

    def _str_(self):
        return f"{self.cnpj} ({'Matriz' if self.is_matrix else 'Filial'})"