from django.db import models
from core.models.company import CompanyBaseModel


class PartnerBaseModel(CompanyBaseModel):
    """
    Base abstrata para parceiros de negócio (clientes e fornecedores).
    
    Implementa os campos comuns para todos os tipos de parceiros,
    facilitando a reutilização de código e padronização.
    """

    class PERSON_TYPE(models.TextChoices):
        PF = 'PF', 'Pessoa Física'
        PJ = 'PJ', 'Pessoa Jurídica'

    class TaxRegime(models.TextChoices):
        SIMPLES = 'simples', 'Simples Nacional'
        SIMPLES_EXCESSO = 'simples_excesso', 'Simples Nacional – Excesso sublimite'
        PRESUMIDO = 'presumido', 'Lucro Presumido'
        REAL = 'real', 'Lucro Real'

    class TaxPayerType(models.TextChoices):
        NON_TAXPAYER = 'non_taxpayer', 'Não Contribuinte'
        TAXPAYER = 'taxpayer', 'Contribuinte'
        EXEMPT = 'exempt', 'Isento'
 
    class PARTNER_TYPE(models.TextChoices):
        CUSTOMER = 'customer', 'Cliente'
        SUPPLIER = 'supplier', 'Fornecedor'

    name = models.CharField(max_length=255, verbose_name='Nome/Razão Social')
    trading_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nome Fantasia')
    cpf_cnpj = models.CharField(max_length=14, verbose_name='CPF/CNPJ')
    person_type = models.CharField(max_length=2, choices=PERSON_TYPE.choices, default=PERSON_TYPE.PF, verbose_name='Tipo de Pessoa')
    partner_type = models.CharField(max_length=10, choices=PARTNER_TYPE.choices, null=True, blank=True, verbose_name='Tipo de Parceiro')
    tax_regime = models.CharField(max_length=20, choices=TaxRegime.choices, blank=True, null=True, verbose_name='Regime Tributário')
    tax_payer_type = models.CharField(max_length=20, choices=TaxPayerType.choices, blank=True, null=True, verbose_name='Tipo de Contribuinte')
    state_registration = models.CharField(max_length=20, blank=True, null=True, verbose_name='Inscrição Estadual')
    municipal_registration = models.CharField(max_length=20, blank=True, null=True, verbose_name='Inscrição Municipal')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Telefone')
    cellphone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Celular')
    address = models.ForeignKey('accounts.Address', on_delete=models.PROTECT, null=True, blank=True, related_name='%(class)ss')
    notes = models.TextField(blank=True, null=True, verbose_name='Observações')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return f"{self.name} - {self.document}"