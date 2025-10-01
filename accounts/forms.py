from allauth.account.forms import LoginForm, SignupForm
from django import forms

from accounts.models.user import User


class CustomLoginForm(LoginForm):
    """Formulário de login customizado com allauth"""

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields["password"].help_text = ""


class CustomSignupForm(SignupForm):
    """Formulário de cadastro customizado com allauth"""

    username = forms.EmailField(label='Email',required=True, help_text='Será necessário validar o e-mail para utilizar o sistema')
    full_name = forms.CharField(max_length=150,label='Nome Completo',required=True)
    agree = forms.BooleanField(
        required=True,
        label='Concordo com os termos e a política',
        help_text='Você deve concordar com os termos para continuar'
    )
    field_order = [
        'full_name',
        'username',
        'password1',
        'agree'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        del self.fields['email']
        self.fields['username'].label = 'Email'
        self.fields['password1'].help_text = None
        self.fields['password1'].widget.attrs.update({'placeholder': ''})

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