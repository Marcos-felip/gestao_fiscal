from django import forms
from django.core.exceptions import ValidationError
from accounts.models.user import Permission, User, Membership


class UserMembershipForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Nome')
    email = forms.EmailField(required=True, label='E-mail')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=True,
        min_length=6,
        max_length=128,
        label='Senha',
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=True,
        min_length=6,
        max_length=128,
        label='Confirmar senha',
    )
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple,
        required=False,
        label='Permissões',
        help_text='Permissões específicas atribuídas a este usuário nesta empresa.'
    )

    class Meta:
        model = Membership
        fields = [
            'name',
            'email',
            'role',
            'permissions',
            'password',
            'password_confirm',
        ]
        labels = {
            'role': 'Função',
        }
        help_texts = {
            'role': 'Função do usuário dentro da empresa.',
        }
    
    def __init__(self, *args, **kwargs):
        self.company_obj = kwargs.pop('company_obj', None)
        super(UserMembershipForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            del self.fields['password']
            del self.fields['password_confirm']
            self.fields['name'].initial = '{} {}'.format(self.instance.user.first_name, self.instance.user.last_name)
            self.fields['email'].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        company = self.data.get('company')
        members = Membership.objects.filter(
            user__email=email,
            company=company
        ).select_related('user')

        if self.instance.pk:
            if self.instance.user.email == email:
                return self.cleaned_data['email'].lower()

        if members.exists():
            raise ValidationError("Já existe um usuário com este e-mail nesta empresa.")

        return self.cleaned_data['email'].lower()

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("As senhas não coincidem.")

        return password_confirm
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        permissions = cleaned_data.get('permissions')
        if role == Membership.Role.MEMBER and not permissions:
            raise ValidationError("Para o papel de 'Membro', você deve selecionar pelo menos uma permissão.")
        return cleaned_data
    
    def save(self, commit=True):
        membership = super().save(commit=False)
        email = self.cleaned_data.get('email').lower()
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')

        user, created = User.objects.get_or_create(email=email)
        if created:
            user.username = email
        if password:
            user.set_password(password)
        if name:
            if ' ' in name:
                first_name, last_name = name.split(' ', 1)
            else:
                first_name, last_name = name, ''
            user.first_name = first_name
            user.last_name = last_name
        user.save()
        membership.user = user
        membership.company = self.company_obj

        if commit:
            membership.save()
            membership.permissions.set(self.cleaned_data['permissions'])
        return membership