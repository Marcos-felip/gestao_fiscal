from django.db import models


class Category(models.Model):
    """
    Modelo para representar categorias de produtos.
    """

    name = models.CharField(max_length=100, verbose_name='Nome da Categoria')
    description = models.TextField(blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name
