from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from django import forms

from accounts.models.company import Company
from accounts.models.user import User


class CustomLoginForm(LoginForm):
    """Formulário de login customizado com allauth"""

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields["password"].help_text = ""

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form'
        self.helper.layout = Layout(
            Field('login', placeholder='seu@email.com', css_class='form-control'),
            Div(
                Div(
                    Field('password', placeholder='Sua senha', css_class='form-control'),
                    css_class='input-group input-group-flat'
                ),
                Div(
                    HTML('<a href="{% url "account_reset_password" %}" class="form-label-description">Esqueci minha senha</a>'),
                    css_class='form-label'
                ),
                css_class='mb-2'
            ),
            Div(
                Field('remember', css_class='form-check-input'),
                css_class='form-check mb-2'
            ),
        )


class CustomSignupForm(SignupForm):
    """Formulário de cadastro customizado com allauth"""

    username = forms.EmailField(label='Email',required=True, help_text='Será necessário validar o e-mail para utilizar o sistema')
    full_name = forms.CharField(max_length=150,label='Nome Completo',required=True)
    field_order = [
        'full_name',
        'username',
        'password1',
        'phone'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        del self.fields['email']
        self.fields['password1'].help_text = None
        self.fields['password1'].widget.attrs.update({'placeholder': ''})

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form'
        self.helper.layout = Layout(
            Field('full_name', placeholder='Seu nome completo', css_class='form-control'),
            Field('username', placeholder='seu@email.com', css_class='form-control'),
            Div(
                Div(
                    Field('password1', placeholder='Sua senha', css_class='form-control'),
                    css_class='input-group input-group-flat'
                ),
                Div(
                    HTML('<div class="form-hint">A senha deve ter pelo menos 8 caracteres</div>'),
                    css_class='form-label'
                ),
                css_class='mb-2'
            ),
            Field('password2', placeholder='Confirme sua senha', css_class='form-control'),
            Submit('submit', 'Cadastrar', css_class='btn btn-primary w-100')
        )

    def clean(self):
        cleaned_data = super(CustomSignupForm, self).clean()
        email = cleaned_data.get('username', '').lower()
        if User.objects.filter(email=email).exists():
           raise forms.ValidationError({"username":["Email já existe",]})
        
        cleaned_data['email'] = email
        return cleaned_data

    def save(self, request):
        full_name = self.cleaned_data.get('full_name')
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = super().save(request)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user
    

class CompanySetupForm(forms.Form):
    """Formulário para configuração inicial da empresa"""

    legal_name = forms.CharField(label='Razão Social', max_length=255)
    slug = forms.SlugField(label='Slug', max_length=255)
    phone = forms.CharField(label='Telefone', max_length=15, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)