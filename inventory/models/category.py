from django.db import models
from core.models.company import CompanyBaseModel


class Category(CompanyBaseModel):
    """
    Modelo para representar categorias de produtos.
    """

    name = models.CharField(max_length=100, verbose_name='Nome da Categoria')
    slug = models.SlugField(verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria de Produto'
        verbose_name_plural = 'Categorias de Produto'
        ordering = ['name']
        indexes = [
            models.Index(fields=['company', 'name']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'slug'],
                name='unique_category_slug_per_company'
            )
        ]

    def __str__(self):
        return self.name
