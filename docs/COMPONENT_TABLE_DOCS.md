# Componente de Tabela - Documentação

## 📍 Localização
- **Template Tag**: `core/templatetags/components.py`
- **Template**: `core/templates/components/common/table.html`

## 🎯 Visão Geral
Componente reutilizável de tabela com card integrado para exibir dados em formato tabular. Ideal para CRUDs e listagens com suporte a customizações, filtros HTMX e ações.

---

## 🚀 Guia de Implementação

### Passo 1: Criar Estrutura de Pastas

```
seu_app/
├── templates/
│   └── seu_app/
│       ├── components/
│       │   └── table_cells.html    # Arquivo único com todas as células
│       └── includes/
│           └── list_view.html       # Partial da tabela
└── views/
    └── list.py
```

### Passo 2: Configurar a View

Adicione o método `get_table_config()` na sua ListView:

```python
from django.views.generic import ListView
from django.urls import reverse_lazy

class ProductListView(ListView):
    model = Product
    template_name = 'products/list_view.html'
    partial_template_name = 'products/includes/list_view.html'
    
    def get_table_config(self):
        """Configuração da tabela de produtos."""
        return {
            # Colunas da tabela
            'headers': [
                {
                    'label': 'Código',
                    'field': 'code',  # Campo simples
                },
                {
                    'label': 'Nome',
                    'field': 'name',
                    'template': 'products/components/table_cells.html',
                    'cell_type': 'name'  # Célula customizada
                },
                {
                    'label': 'Categoria',
                    'field': 'category.name',  # Nested field
                },
                {
                    'label': 'Preço',
                    'field': 'price',
                    'template': 'products/components/table_cells.html',
                    'cell_type': 'price'
                },
                {
                    'label': 'Status',
                    'field': 'is_active',
                    'template': 'products/components/table_cells.html',
                    'cell_type': 'status'
                },
            ],
            
            # Ações de cada linha
            'actions_template': 'products/components/table_cells.html',
            'actions_cell_type': 'actions',
            
            # Configurações do card
            'card_title': 'Lista de Produtos',
            'card_actions': [
                {
                    'label': 'Novo Produto',
                    'url': reverse_lazy('products:create'),
                    'icon': '<svg>...</svg>',
                    'class': 'btn-primary'
                }
            ],
            
            # Configurações extras
            'table_id': 'products-table',
            'empty_message': 'Nenhum produto cadastrado.'
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_config'] = self.get_table_config()
        return context
    
    def render_to_response(self, context, **response_kwargs):
        # Para suportar HTMX
        if self.request.headers.get('Hx-Request'):
            self.template_name = self.partial_template_name
        return super().render_to_response(context, **response_kwargs)
```

### Passo 3: Criar Template de Células

Crie um único arquivo `table_cells.html` com todas as customizações:

```django
{# products/components/table_cells.html #}

{% if cell_type == 'name' %}
    {# Célula customizada de nome com ícone #}
    <div class="d-flex align-items-center">
        <svg class="icon me-2">...</svg>
        <strong>{{ object.name }}</strong>
    </div>

{% elif cell_type == 'price' %}
    {# Célula de preço formatado #}
    <span class="text-success">
        R$ {{ object.price|floatformat:2 }}
    </span>

{% elif cell_type == 'status' %}
    {# Célula de status com badge #}
    {% if object.is_active %}
        <span class="badge bg-green-lt">Ativo</span>
    {% else %}
        <span class="badge bg-red-lt">Inativo</span>
    {% endif %}

{% elif cell_type == 'actions' %}
    {# Célula de ações #}
    <div class="btn-list flex-nowrap">
        <a href="{% url 'products:edit' object.pk %}" 
           class="btn btn-ghost-primary btn-icon"
           title="Editar">
            <svg>...</svg>
        </a>
        <button class="btn btn-ghost-danger btn-icon"
                data-bs-toggle="modal"
                data-bs-target="#deleteModal-{{ object.pk }}"
                title="Excluir">
            <svg>...</svg>
        </button>
    </div>

{% endif %}
```

### Passo 4: Criar Template Partial

```django
{# products/includes/list_view.html #}
{% load components %}

{% render_table headers=table_config.headers rows=object_list actions_template=table_config.actions_template actions_cell_type=table_config.actions_cell_type empty_message=table_config.empty_message card_title=table_config.card_title card_actions=table_config.card_actions table_id=table_config.table_id %}
```

### Passo 5: Usar no Template Principal

```django
{# products/list_view.html #}
{% extends "base.html" %}

{% block content %}
<div class="page-body px-4">
    {# Filtros (opcional) #}
    <div class="card mb-3">
        <div class="card-body">
            <form hx-get="{% url 'products:list' %}" 
                  hx-target="#products-table" 
                  hx-swap="innerHTML">
                <input type="text" name="search" placeholder="Buscar...">
                <button type="submit">Buscar</button>
            </form>
        </div>
    </div>

    {# Tabela #}
    {% include "products/includes/list_view.html" %}
</div>
{% endblock %}
```

---

## 📖 Referência de Parâmetros

### `render_table`

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `headers` | list | ✅ | Configuração das colunas |
| `rows` | QuerySet/list | ✅ | Dados a serem exibidos |
| `actions_template` | str | ❌ | Template de ações por linha |
| `actions_cell_type` | str | ❌ | Tipo da célula de ações |
| `empty_message` | str | ❌ | Mensagem quando vazio (padrão: "Nenhum registro encontrado.") |
| `row_class_field` | str | ❌ | Campo para classe CSS da linha |
| `card_title` | str | ❌ | Título do card |
| `card_actions` | list | ❌ | Botões do header |
| `table_id` | str | ❌ | ID para HTMX target |

### Configuração de Header

```python
{
    'label': 'Título da Coluna',      # Obrigatório
    'field': 'campo.nested',          # Obrigatório (ou use template)
    'template': 'path/to/cells.html', # Opcional
    'cell_type': 'tipo',              # Opcional (quando usa template)
    'width': 'w-10',                  # Opcional (classe CSS)
}
```

### Configuração de Card Action

Cada ação do card é um dicionário com:

```python
{
    'label': 'Texto do Botão',           # Obrigatório
    'url': reverse_lazy('app:view'),     # Obrigatório
    'variant': 'primary',                # Opcional (padrão: 'primary')
    'icon': '<svg>...</svg>',            # Opcional
    'size': 'sm',                        # Opcional (sm, lg)
    'extra_classes': 'my-class',         # Opcional
}
```

**Nota**: O campo `class` ainda é suportado para retrocompatibilidade (será convertido para `variant`).

---

## 💡 Exemplos de Uso

### Tabela Simples (sem customizações)

```python
def get_table_config(self):
    return {
        'headers': [
            {'label': 'Nome', 'field': 'name'},
            {'label': 'Email', 'field': 'email'},
            {'label': 'Telefone', 'field': 'phone'},
        ],
        'card_title': 'Contatos',
    }
```

### Tabela com Campos Nested

```python
def get_table_config(self):
    return {
        'headers': [
            {'label': 'Produto', 'field': 'name'},
            {'label': 'Categoria', 'field': 'category.name'},
            {'label': 'Fornecedor', 'field': 'supplier.company.name'},
            {'label': 'Status', 'field': 'get_status_display'},  # Método choice
        ],
    }
```

### Tabela com Múltiplas Ações no Header

```python
def get_table_config(self):
    return {
        'headers': [...],
        'card_title': 'Relatórios',
        'card_actions': [
            {
                'label': 'Exportar PDF',
                'url': reverse_lazy('reports:export_pdf'),
                'class': 'btn-outline-danger'
            },
            {
                'label': 'Exportar Excel',
                'url': reverse_lazy('reports:export_excel'),
                'class': 'btn-outline-success'
            },
            {
                'label': 'Novo Relatório',
                'url': reverse_lazy('reports:create'),
                'variant': 'primary',
                'icon': '<svg>...</svg>'
            },
        ],
    }
```

---

## 🎨 Dicas e Boas Práticas

### ✅ Use um arquivo único de células
Crie `table_cells.html` com blocos condicionais em vez de múltiplos arquivos.

### ✅ Aproveite campos nested
```python
'field': 'user.company.name'  # Acessa object.user.company.name
```

### ✅ Use width para colunas específicas
```python
{'label': 'ID', 'field': 'id', 'width': 'w-1'}  # Coluna estreita
```

### ✅ Integre com HTMX para filtros
```python
'table_id': 'my-table'  # Permite hx-target="#my-table"
```

### ✅ Reutilize o mesmo template de células
```python
'template': 'products/components/table_cells.html',
'cell_type': 'price'  # Diferencia pelo cell_type
```

---

## 🔧 Estrutura HTML Gerada

```html
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Título</h3>
        <div class="card-actions">
            <a href="..." class="btn btn-primary">
                <svg>...</svg>
                Novo
            </a>
        </div>
    </div>
    <div class="table-responsive" id="table-id">
        <table class="table table-vcenter table-mobile-md card-table">
            <thead>...</thead>
            <tbody>...</tbody>
        </table>
    </div>
</div>
```
