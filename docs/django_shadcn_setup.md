# Django Shadcn - Guia de Configuração e Uso

Este documento descreve como utilizar o sistema de componentes **shadcn** no projeto Django, integrado com **Tailwind CSS** e **django-cotton**.

## 📦 Dependências Instaladas

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| `django-cotton` | 2.6.0 | Componentes HTML-like para Django |
| `django-tailwind-cli` | 4.5.1 | Integração Tailwind CSS sem Node.js |
| `crispy-tailwind` | 1.0.4 | Template pack Tailwind para crispy-forms |

## 🏗️ Estrutura de Arquivos

```
gestao_fiscal/
├── input.css                    # Arquivo fonte do Tailwind CSS
├── static/
│   └── css/
│       └── output.css           # CSS compilado (gerado automaticamente)
├── templates/
│   └── cotton/                  # Componentes shadcn (django-cotton)
│       ├── avatar/
│       ├── badge/
│       ├── button/
│       ├── card/
│       ├── dialog/
│       ├── dropdown_menu/
│       ├── input/
│       ├── table/
│       └── toast/
└── .django_tailwind_cli/        # Binário do Tailwind (ignorado pelo Git)
    └── tailwindcss-linux-x64-*  # Executável baixado automaticamente
```

## ⚙️ Configuração no `settings.py`

### Apps Instalados

```python
INSTALLED_APPS = [
    # ...
    'django_cotton',          # Componentes HTML-like
    'django_tailwind_cli',    # Tailwind CSS CLI
    'crispy_forms',           # Forms estilizados
    'crispy_tailwind',        # Template pack Tailwind
    # ...
]
```

### Configurações do Tailwind CLI

```python
# Tailwind CSS
TAILWIND_CLI_SRC_CSS = 'input.css'           # Arquivo fonte
TAILWIND_CLI_DIST_CSS = 'css/output.css'     # Arquivo de saída em static/
TAILWIND_CLI_CONFIG_FILE = None              # Usa configuração do input.css
```

### Configurações do Crispy Forms

```python
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"
```

---

## 🔨 Comandos de Build

### Build de Produção

Compila o CSS uma única vez, minificado para produção:

```bash
python manage.py tailwind build
```

### Build com Force

Força a recompilação mesmo se não houver mudanças:

```bash
python manage.py tailwind build --force
```

### Watch Mode (Desenvolvimento)

Monitora mudanças e recompila automaticamente:

```bash
python manage.py tailwind watch
```

> **Dica:** Em desenvolvimento, rode `tailwind watch` em um terminal separado enquanto o servidor Django roda em outro.

### Download do Binário

O binário do Tailwind é baixado automaticamente na primeira execução. Para baixar manualmente:

```bash
python manage.py tailwind download
```

---

## 🧩 Usando Componentes Cotton (shadcn)

### Sintaxe Básica

Os componentes usam a sintaxe `<c-nome-componente>`:

```html
<!-- Botão -->
<c-button>Clique aqui</c-button>

<!-- Botão com variante -->
<c-button variant="destructive">Excluir</c-button>

<!-- Card -->
<c-card>
    <c-card.header>
        <c-card.title>Título</c-card.title>
        <c-card.description>Descrição</c-card.description>
    </c-card.header>
    <c-card.content>
        Conteúdo do card
    </c-card.content>
</c-card>
```

### Componentes Disponíveis

#### Button
```html
<c-button>Default</c-button>
<c-button variant="secondary">Secondary</c-button>
<c-button variant="destructive">Destructive</c-button>
<c-button variant="outline">Outline</c-button>
<c-button variant="ghost">Ghost</c-button>
<c-button variant="link">Link</c-button>
<c-button size="sm">Pequeno</c-button>
<c-button size="lg">Grande</c-button>
<c-button size="icon">🔍</c-button>
```

#### Badge
```html
<c-badge>Default</c-badge>
<c-badge variant="secondary">Secondary</c-badge>
<c-badge variant="destructive">Destructive</c-badge>
<c-badge variant="outline">Outline</c-badge>
```

#### Input
```html
<c-input type="text" placeholder="Digite aqui..." />
<c-input type="email" placeholder="email@exemplo.com" />
<c-input type="password" placeholder="Senha" />
```

#### Table
```html
<c-table>
    <c-table.header>
        <c-table.row>
            <c-table.head>Nome</c-table.head>
            <c-table.head>Email</c-table.head>
        </c-table.row>
    </c-table.header>
    <c-table.body>
        <c-table.row>
            <c-table.cell>João</c-table.cell>
            <c-table.cell>joao@email.com</c-table.cell>
        </c-table.row>
    </c-table.body>
</c-table>
```

#### Card
```html
<c-card>
    <c-card.header>
        <c-card.title>Título do Card</c-card.title>
        <c-card.description>Descrição opcional</c-card.description>
    </c-card.header>
    <c-card.content>
        Conteúdo principal do card
    </c-card.content>
    <c-card.footer>
        <c-button>Ação</c-button>
    </c-card.footer>
</c-card>
```

#### Dialog (Modal)
```html
<c-dialog>
    <c-dialog.trigger>
        <c-button>Abrir Modal</c-button>
    </c-dialog.trigger>
    <c-dialog.content>
        <c-dialog.header>
            <c-dialog.title>Título</c-dialog.title>
            <c-dialog.description>Descrição do modal</c-dialog.description>
        </c-dialog.header>
        <div>Conteúdo do modal</div>
        <c-dialog.footer>
            <c-button variant="outline">Cancelar</c-button>
            <c-button>Confirmar</c-button>
        </c-dialog.footer>
    </c-dialog.content>
</c-dialog>
```

---

## 📝 Criando Novos Componentes

### 1. Criar a Estrutura de Pastas

```bash
mkdir -p templates/cotton/nome_componente
```

### 2. Criar o Arquivo Principal (`index.html`)

```html
<!-- templates/cotton/nome_componente/index.html -->
<div {{ attrs }} class="classe-base {{ class }}">
    {{ slot }}
</div>
```

### 3. Criar Sub-componentes (opcional)

```html
<!-- templates/cotton/nome_componente/header.html -->
<div class="classe-header {{ class }}">
    {{ slot }}
</div>
```

### 4. Usar o Componente

```html
<c-nome_componente class="classe-extra">
    <c-nome_componente.header>Título</c-nome_componente.header>
    Conteúdo
</c-nome_componente>
```

### Convenções

- **Nome do diretório**: snake_case (ex: `dropdown_menu`)
- **Uso no template**: com underscore (ex: `<c-dropdown_menu>`)
- **Arquivo principal**: sempre `index.html`
- **Sub-componentes**: arquivos separados no mesmo diretório

---

## 🎨 Configuração do Tailwind CSS

### Arquivo `input.css`

```css
@import "tailwindcss";

/* Configuração de cores e variáveis CSS */
@theme {
    --color-border: oklch(0.922 0.004 286.32);
    --color-input: oklch(0.922 0.004 286.32);
    --color-ring: oklch(0.871 0.006 286.286);
    --color-background: oklch(1 0 0);
    --color-foreground: oklch(0.141 0.005 285.823);
    /* ... outras variáveis */
}

/* Modo escuro */
.dark {
    --color-background: oklch(0.141 0.005 285.823);
    --color-foreground: oklch(0.985 0 0);
    /* ... */
}

/* Source para escanear classes */
@source "../templates/**/*.html";
@source "../**/templates/**/*.html";
```

### Adicionar Novas Classes

Se você usar classes Tailwind que não estão sendo detectadas:

1. Adicione a classe em um arquivo `.html` dentro dos diretórios configurados em `@source`
2. Ou adicione manualmente no `input.css`:

```css
@layer utilities {
    .minha-classe-customizada {
        /* estilos */
    }
}
```

3. Rode o build novamente:
```bash
python manage.py tailwind build --force
```

---

## 🔄 Workflow de Desenvolvimento

### 1. Iniciar o Ambiente

```bash
# Terminal 1 - Servidor Django
source venv/bin/activate
python manage.py runserver

# Terminal 2 - Tailwind Watch
source venv/bin/activate
python manage.py tailwind watch
```

### 2. Criar/Editar Templates

Edite os templates normalmente. O Tailwind vai detectar as classes e recompilar.

### 3. Adicionar Novos Componentes

```bash
# Criar estrutura
mkdir -p templates/cotton/meu_componente

# Criar arquivo principal
touch templates/cotton/meu_componente/index.html
```

### 4. Antes de Commit

```bash
# Build final para produção
python manage.py tailwind build --force

# Verificar se output.css foi atualizado
git status
```

---

## 🐛 Troubleshooting

### Erro: "TemplateDoesNotExist"

1. Verifique se o componente existe em `templates/cotton/`
2. Verifique o nome (use underscore, não hífen)
3. Verifique se `django_cotton` está em `INSTALLED_APPS`

### Classes CSS não aplicadas

1. Verifique se a classe está no arquivo compilado:
```bash
grep "nome-da-classe" static/css/output.css
```

2. Force rebuild:
```bash
python manage.py tailwind build --force
```

3. Verifique os paths em `@source` no `input.css`

### Binário do Tailwind não encontrado

```bash
# Baixar novamente
python manage.py tailwind download

# Ou remover e deixar baixar automaticamente
rm -rf .django_tailwind_cli/
python manage.py tailwind build
```

### Conflito com Bootstrap/Tabler

Se houver conflito de estilos, certifique-se de que:
1. Não há CDN do Bootstrap nos templates
2. Não há CSS do Tabler importado
3. Use apenas as classes Tailwind

---

## 📚 Referências

- [django-cotton Docs](https://django-cotton.com/)
- [django-tailwind-cli Docs](https://django-tailwind-cli.andrich.me/)
- [Tailwind CSS v4 Docs](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [Crispy Tailwind](https://github.com/django-crispy-forms/crispy-tailwind)

---

## 📋 Checklist de Deploy

- [ ] Rodar `python manage.py tailwind build --force`
- [ ] Verificar se `static/css/output.css` está atualizado
- [ ] Verificar se `.django_tailwind_cli/` está no `.gitignore`
- [ ] Coletar arquivos estáticos: `python manage.py collectstatic`
- [ ] Testar todas as páginas migradas para shadcn
