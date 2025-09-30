from django.db import models
from django.utils import timezone


class Address(models.Model):
    """Endereço físico normalizado utilizado por estabelecimentos."""
    street = models.CharField(max_length=255, verbose_name='Logradouro')
    number = models.CharField(max_length=20, verbose_name='Número')
    complement = models.CharField(max_length=60, blank=True, verbose_name='Complemento')
    district = models.CharField(max_length=80, verbose_name='Bairro')
    city_name = models.CharField(max_length=120, verbose_name='Cidade')
    city_ibge_code = models.CharField(max_length=7, help_text='Código IBGE (7 dígitos)', verbose_name='Código IBGE')
    state = models.CharField(max_length=2, verbose_name='UF')
    postal_code = models.CharField(max_length=8, help_text='CEP (8 dígitos)', verbose_name='CEP')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        indexes = [
            models.Index(fields=['city_ibge_code']),
            models.Index(fields=['state']),
        ]

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city_name}/{self.state}"
