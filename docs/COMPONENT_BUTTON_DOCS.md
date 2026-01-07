# Componente de Botão - Documentação

## 📍 Localização
- **Template Tag**: `core/templatetags/components.py`
- **Template**: `core/templates/components/ui/button.html`

## 🎯 Visão Geral
Componente reutilizável de botão que suporta diversos estilos, tamanhos, ícones e pode ser renderizado como `<button>` ou `<a>`.

---

## 🚀 Uso Básico

```django
{% load components %}

{# Botão simples #}
{% render_button label="Salvar" variant="primary" %}

{# Botão com ícone #}
{% render_button label="Novo" variant="primary" icon="<svg>...</svg>" %}

{# Link estilizado como botão #}
{% render_button label="Ver Detalhes" variant="outline-primary" href="/detalhes/1" %}

{# Botão apenas com ícone #}
{% render_button label="Editar" variant="ghost-primary" icon_only=True icon="<svg>...</svg>" %}
```

---

## 📖 Parâmetros

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `label` | str | - | ✅ **Obrigatório** - Texto do botão (ou título para acessibilidade quando icon_only) |
| `variant` | str | `'primary'` | Estilo do botão (ver variantes abaixo) |
| `size` | str | `None` | Tamanho: `'sm'`, `'lg'` |
| `type` | str | `'button'` | Tipo: `'button'`, `'submit'`, `'reset'` |
| `icon` | str | `None` | SVG do ícone (inline) |
| `icon_only` | bool | `False` | True para exibir apenas o ícone |
| `href` | str | `None` | URL - renderiza como `<a>` em vez de `<button>` |
| `extra_classes` | str | `None` | Classes CSS adicionais |
| `attrs` | dict | `{}` | Atributos HTML extras |
| `disabled` | bool | `False` | True para desabilitar |

---

## 🎨 Variantes de Estilo

### Variantes Sólidas
- `primary` - Botão primário (azul)
- `secondary` - Botão secundário (cinza)
- `success` - Sucesso (verde)
- `danger` - Perigo (vermelho)
- `warning` - Aviso (amarelo)
- `info` - Informação (ciano)

### Variantes Ghost
- `ghost-primary`
- `ghost-secondary`
- `ghost-success`
- `ghost-danger`
- `ghost-warning`
- `ghost-info`

### Variantes Outline
- `outline-primary`
- `outline-secondary`
- `outline-success`
- `outline-danger`
- `outline-warning`
- `outline-info`

---

## 💡 Exemplos Práticos

### Botão de Submit em Formulário

```django
{% load components %}

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    
    {% render_button 
        label="Salvar" 
        variant="primary" 
        type="submit" 
        icon='<svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M6 4h10l4 4v10a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2" /></svg>'
    %}
</form>
```

### Botão de Ação com Modal

```django
{% render_button 
    label="Excluir" 
    variant="danger" 
    attrs=attrs_dict
%}

{# Na view ou context #}
attrs_dict = {
    'data-bs-toggle': 'modal',
    'data-bs-target': '#deleteModal-123'
}
```

### Link Estilizado como Botão

```django
{% render_button 
    label="Editar Produto" 
    variant="primary" 
    href="{% url 'products:edit' product.pk %}"
    icon='<svg>...</svg>'
%}
```

### Botão Apenas com Ícone (Icon Button)

```django
{# Botão de editar #}
{% render_button 
    label="Editar" 
    variant="ghost-primary" 
    icon_only=True 
    href="{% url 'users:edit' user.pk %}"
    icon='<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-edit" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M7 7h-1a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-1" /><path d="M20.385 6.585a2.1 2.1 0 0 0 -2.97 -2.97l-8.415 8.385v3h3l8.385 -8.415z" /><path d="M16 5l3 3" /></svg>'
    attrs=tooltip_attrs
%}

{# tooltip_attrs = {'data-bs-toggle': 'tooltip', 'title': 'Editar'} #}
```

### Grupo de Botões

```django
<div class="btn-list">
    {% render_button label="Salvar" variant="primary" type="submit" %}
    {% render_button label="Cancelar" variant="secondary" href="{% url 'products:list' %}" %}
</div>
```

### Botão Pequeno

```django
{% render_button 
    label="Ver Mais" 
    variant="outline-primary" 
    size="sm"
    href="{% url 'details' %}"
%}
```

### Botão Desabilitado

```django
{% render_button 
    label="Processar" 
    variant="primary" 
    disabled=True
%}
```

### Botão com Classes Extras

```django
{% render_button 
    label="Upload" 
    variant="success" 
    extra_classes="w-100 mt-3"
    icon='<svg>...</svg>'
%}
```

---

## 🔧 Uso em Context/View

Você pode preparar configurações de botões na view:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Configuração de botão de ação
    context['edit_button'] = {
        'label': 'Editar',
        'variant': 'primary',
        'href': reverse('products:edit', args=[self.object.pk]),
        'icon': '<svg>...</svg>'
    }
    
    # Botão com atributos
    context['delete_button'] = {
        'label': 'Excluir',
        'variant': 'danger',
        'attrs': {
            'data-bs-toggle': 'modal',
            'data-bs-target': f'#deleteModal-{self.object.pk}'
        }
    }
    
    return context
```

No template:

```django
{% render_button 
    label=edit_button.label 
    variant=edit_button.variant 
    href=edit_button.href 
    icon=edit_button.icon 
%}

{% render_button 
    label=delete_button.label 
    variant=delete_button.variant 
    attrs=delete_button.attrs 
%}
```

---

## 🎨 Exemplos de Ícones SVG

### Ícone de Adicionar
```html
<svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
    <path d="M12 5l0 14" />
    <path d="M5 12l14 0" />
</svg>
```

### Ícone de Editar
```html
<svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
    <path d="M7 7h-1a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-1" />
    <path d="M20.385 6.585a2.1 2.1 0 0 0 -2.97 -2.97l-8.415 8.385v3h3l8.385 -8.415z" />
    <path d="M16 5l3 3" />
</svg>
```

### Ícone de Excluir
```html
<svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
    <path d="M4 7l16 0" />
    <path d="M10 11l0 6" />
    <path d="M14 11l0 6" />
    <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" />
    <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" />
</svg>
```

---

## ✨ Dicas

### ✅ Use variant apropriado
- `primary` para ações principais
- `success` para confirmações
- `danger` para ações destrutivas
- `ghost-*` para ações secundárias menos chamativas
- `outline-*` para botões sem preenchimento

### ✅ Icon buttons para economia de espaço
Ótimo para tabelas e toolbars:
```django
{% render_button label="Editar" variant="ghost-primary" icon_only=True icon="<svg>...</svg>" %}
```

### ✅ Combine com tooltips
```django
{% render_button 
    label="Ajuda" 
    variant="ghost-info" 
    icon_only=True 
    icon="<svg>...</svg>"
    attrs=tooltip
%}
{# tooltip = {'data-bs-toggle': 'tooltip', 'title': 'Clique para ajuda'} #}
```

### ✅ Mantenha ícones em variáveis
Crie um arquivo de ícones reutilizáveis para evitar repetição de SVG.

---

## 🔧 Estrutura HTML Gerada

### Botão
```html
<button type="submit" class="btn btn-primary">
    <svg>...</svg>
    Salvar
</button>
```

### Link como Botão
```html
<a href="/edit/1" class="btn btn-outline-primary">
    <svg>...</svg>
    Editar
</a>
```

### Icon Button
```html
<button type="button" class="btn btn-ghost-primary btn-icon">
    <svg>...</svg>
</button>
```
