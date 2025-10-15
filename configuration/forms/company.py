from django import forms
from accounts.models.company import Establishment


class CompanyForm(forms.ModelForm):
    legal_name = forms.CharField(max_length=255, label='Razão Social', required=True)
    trade_name = forms.CharField(max_length=255, label='Nome Fantasia', required=False)
    cnpj = forms.CharField(max_length=14, label='CNPJ', required=True)
    state_registration = forms.CharField(max_length=20, label='Inscrição Estadual', required=False, help_text='Inscrição Estadual do estabelecimento.')
    municipal_registration = forms.CharField(max_length=20, label='Inscrição Municipal', required=False, help_text='Inscrição Municipal do estabelecimento.')
    phone = forms.CharField(max_length=15, label='Telefone', required=False, help_text='Telefone do estabelecimento.')
    environment_default = forms.ChoiceField(choices=Establishment.Environment.choices, label='Ambiente Padrão', required=True, help_text='Ambiente padrão para emissão de documentos fiscais.')

    class Meta:
        model = Establishment
        fields = [
            'legal_name',
            'trade_name',
            'cnpj',
            'state_registration',
            'municipal_registration',
            'address', 
            'phone', 
            'is_matrix', 
            'environment_default'
        ]
        labels = {
            'cnpj': 'CNPJ',
            'state_registration': 'Inscrição Estadual',
            'municipal_registration': 'Inscrição Municipal',
            'address': 'Endereço',
            'phone': 'Telefone',
            'is_matrix': 'É Matriz?',
            'environment_default': 'Ambiente Padrão',
        }
        help_texts = {
            'is_matrix': 'Indica se este estabelecimento é a matriz da empresa.',
        }


    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if self.company:
            self.fields['legal_name'].initial = self.company.legal_name
            self.fields['trade_name'].initial = self.company.trade_name

    def save(self, commit=True):
        if self.company:
            self.company.legal_name = self.cleaned_data['legal_name']
            self.company.trade_name = self.cleaned_data['trade_name']
            self.company.save()
        establishment = super().save(commit=False)
        establishment.company = self.company
        if commit:
            establishment.save()
        return establishment


