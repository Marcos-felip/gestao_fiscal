from django import forms
from inventory.models.category import Category


class CategoryForm(forms.ModelForm):
    """Formulário para criação e edição de categorias de produtos"""

    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nome da Categoria'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Slug da Categoria'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Descrição da Categoria', 'rows': 3})

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        company = self.instance.company if self.instance.pk else self.initial.get('company')

        if Category.objects.filter(company=company, slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Já existe uma categoria com este slug nesta empresa.")
        
        return slug
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        company = self.instance.company if self.instance.pk else self.initial.get('company')

        if Category.objects.filter(company=company, name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Já existe uma categoria com este nome nesta empresa.")
        
        return name
