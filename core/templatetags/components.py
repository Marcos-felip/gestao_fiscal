from django import template

register = template.Library()


@register.inclusion_tag('components/common/table.html')
def render_table(headers, rows, actions_template=None, actions_cell_type=None, 
                empty_message="Nenhum registro encontrado.", row_class_field=None,
                card_title=None, card_actions=None, table_id=None):
    """
    Renderiza uma tabela reutilizável dentro de um card.
    
    Args:
        card_title: (opcional) Título do card
        card_actions: (opcional) Lista de ações do card header (botões)
        table_id: (opcional) ID do elemento table-responsive para HTMX
        headers: Lista de dicionários com as configurações das colunas:
            - label: Texto do cabeçalho
            - field: Nome do atributo do objeto (suporta nested com ponto, ex: 'user.email')
            - template: (opcional) Template customizado para renderizar a célula
            - cell_type: (opcional) Tipo de célula quando usando arquivo com blocos condicionais
            - width: (opcional) Classe CSS para largura da coluna
        rows: QuerySet ou lista de objetos a serem exibidos
        actions_template: (opcional) Template para renderizar as ações de cada linha
        actions_cell_type: (opcional) Tipo de célula de ações quando usando arquivo com blocos
        empty_message: Mensagem exibida quando não há registros
        row_class_field: (opcional) Campo do objeto para adicionar classe CSS na linha
    Exemplo de uso:
        {% load components %}
        {% render_table card_title=table_config.card_title card_actions=table_config.card_actions table_id="users-table" table_config.headers object_list table_config.actions_template table_config.actions_cell_type %}
    """
    return {
        'card_title': card_title,
        'card_actions': card_actions,
        'table_id': table_id,
        'headers': headers,
        'rows': rows,
        'actions_template': actions_template,
        'actions_cell_type': actions_cell_type,
        'empty_message': empty_message,
        'row_class_field': row_class_field,
    }


@register.filter
def get_attr(obj, attr_name):
    """
    Obtém um atributo de um objeto dinamicamente.
    Suporta nested attributes usando ponto (ex: 'user.email')
    
    Uso:
        {{ object|get_attr:"user.email" }}
        {{ object|get_attr:"get_status_display" }}
    """
    if not attr_name:
        return ''
    
    attrs = str(attr_name).split('.')
    value = obj
    
    for attr in attrs:
        if value is None:
            return ''
            
        # Tenta acessar como atributo
        if hasattr(value, attr):
            value = getattr(value, attr)
        # Tenta acessar como dicionário
        elif hasattr(value, 'get') and callable(value.get):
            value = value.get(attr, '')
        else:
            return ''
    
    # Se for um método, chama ele
    if callable(value):
        try:
            value = value()
        except TypeError:
            # Método requer argumentos
            return ''
    
    return value if value is not None else ''


@register.filter
def add_one(value):
    """
    Adiciona 1 ao valor.
    Útil para calcular colspan da tabela.
    
    Uso:
        {{ headers|length|add_one }}
    """
    try:
        return int(value) + 1
    except (ValueError, TypeError):
        return value


@register.inclusion_tag('components/ui/button.html')
def render_button(label, variant='primary', size=None, type='button', icon=None, 
                 icon_only=False, href=None, extra_classes=None, attrs=None, disabled=False):
    """
    Renderiza um botão reutilizável.
    
    Args:
        label: Texto do botão
        variant: Estilo (primary, secondary, success, danger, warning, info, ghost-primary, outline-primary, etc.)
        size: Tamanho (sm, md, lg) - opcional
        type: Tipo do botão (button, submit, reset) - padrão: button
        icon: SVG do ícone - opcional
        icon_only: True para botão apenas com ícone (adiciona classe btn-icon)
        href: URL para renderizar como link <a> em vez de <button>
        extra_classes: Classes CSS adicionais
        attrs: Dicionário de atributos HTML extras (data-bs-toggle, etc.)
        disabled: True para desabilitar o botão
    
    Exemplo de uso:
        {% load components %}
        {% render_button label="Salvar" variant="primary" icon="<svg>...</svg>" %}
        {% render_button label="Editar" variant="ghost-primary" icon_only=True href="/edit/1" %}
    """
    return {
        'label': label,
        'variant': variant,
        'size': size,
        'type': type,
        'icon': icon,
        'icon_only': icon_only,
        'href': href,
        'extra_classes': extra_classes,
        'attrs': attrs or {},
        'disabled': disabled,
    }
