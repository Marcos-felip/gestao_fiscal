from django.db import models


class Unit(models.Model):
    """
    Modelo para representar unidades de medida de produtos.
    """

    name = models.CharField(max_length=100, verbose_name='Nome da Unidade')
    abbreviation = models.CharField(max_length=10, verbose_name='Abreviação')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"
