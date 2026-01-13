# Gestão Fiscal

Sistema de gestão fiscal desenvolvido com Django para controle e administração de empresas.

## 🚀 Funcionalidades

- Autenticação de usuários com Django Allauth
- Interface moderna com **shadcn/ui** + **Tailwind CSS**
- Componentes reutilizáveis com **django-cotton**
- Formulários estilizados com Crispy Forms + Tailwind
- Sistema multi-empresa com estabelecimentos
- CRUD completo: Clientes, Fornecedores, Produtos, Categorias, Unidades

## 📋 Pré-requisitos

- Python 3.11+
- PostgreSQL (recomendado) ou outro banco de dados suportado pelo Django

## 🛠️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Marcos-felip/gestao_fiscal.git
   cd gestao_fiscal
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**
   - Crie o arquivo `gestao_fiscal/local_settings.py` com suas configurações:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'gestao_fiscal',
           'USER': 'seu_usuario',
           'PASSWORD': 'sua_senha',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
   
5. **Execute as migrações:**
   ```bash
   python manage.py migrate
   ```

6. **Compile o Tailwind CSS:**
   ```bash
   python manage.py tailwind build
   ```
   > O binário do Tailwind será baixado automaticamente na primeira execução.

7. **Execute o servidor:**
   ```bash
   python manage.py runserver
   ```

8. **Acesse:** http://127.0.0.1:8000/

## 💻 Desenvolvimento

Para desenvolvimento, rode o Tailwind em modo watch para recompilar automaticamente:

```bash
# Terminal 1 - Servidor Django
source venv/bin/activate
python manage.py runserver

# Terminal 2 - Tailwind Watch
source venv/bin/activate
python manage.py tailwind watch
```

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Django | 5.2.6 | Framework web Python |
| django-cotton | 2.6.0 | Componentes HTML-like |
| django-tailwind-cli | 4.5.1 | Tailwind CSS sem Node.js |
| crispy-tailwind | 1.0.4 | Formulários com Tailwind |
| Django Allauth | - | Autenticação |
| HTMX | 1.9.10 | Interatividade sem JavaScript |
| Alpine.js | 3.x | Reatividade leve |
| PostgreSQL | - | Banco de dados |

## 📁 Estrutura do Projeto

```
gestao_fiscal/
├── accounts/          # Autenticação e usuários
├── configuration/     # Configurações do sistema
├── core/              # Modelos base compartilhados
├── customers/         # Módulo de clientes (em partners/)
├── suppliers/         # Módulo de fornecedores (em partners/)
├── inventory/         # Produtos, categorias, unidades
├── templates/
│   └── cotton/        # Componentes shadcn
├── static/
│   └── css/
│       └── output.css # CSS compilado
├── input.css          # Fonte do Tailwind
└── docs/              # Documentação adicional
```
