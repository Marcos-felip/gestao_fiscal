# Gestão Fiscal

Sistema de gestão fiscal desenvolvido com Django para controle e administração de empresas.

## 🚀 Funcionalidades

- Autenticação de usuários com Allauth
- Interface moderna com Tabler.io
- Formulários simplificados com Crispy Forms
- Sistema de contas e empresas

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
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**
   - Edite `gestao_fiscal/local_settings.py` com suas configurações de banco
   - Execute as migrações:
   ```bash
   python manage.py migrate
   ```

5. **Execute o servidor:**
   ```bash
   python manage.py runserver
   ```

6. **Acesse:** http://127.0.0.1:8000/

## 🛠️ Tecnologias Utilizadas

- **Backend:** Django 5.2.6
- **Frontend:** Tabler.io (Bootstrap-based)
- **Autenticação:** Django Allauth
- **Formulários:** Crispy Forms + Bootstrap 5
- **Banco:** PostgreSQL
