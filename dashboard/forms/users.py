from django import forms
from django.core.exceptions import ValidationError
from accounts.models.user import User, Membership


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

    class Meta:
        model = Membership
        fields = [
            'role',
            'name',
            'email',
            'password',
            'password_confirm'
        ]
    
    def __init__(self, *args, **kwargs):
        self.company_obj = kwargs.pop('company_obj', None)
        super().__init__(*args, **kwargs)
        

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
    
    def save(self, commit=True):
        membership = super().save(commit=False)
        email = self.cleaned_data.get('email').lower()
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')

        user, created = User.objects.get_or_create(email=email)
        if created:
            user.username = email
            user.set_password(password)
            if ' ' in name:
                first_name, last_name = name.split(' ', 1)
            else:
                first_name, last_name = name, ''
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        membership.user = user

        if commit:
            membership.save()
        return membership