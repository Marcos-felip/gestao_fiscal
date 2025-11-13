from django import forms
from partners.models.customers import Customer
from core import widgets


class CustomerBasicForm(forms.ModelForm):
    cpf = forms.CharField(max_length=11, label='CPF', required=False)
    cnpj = forms.CharField(max_length=14, label='CNPJ', required=False)
    email = forms.EmailField(required=True)
    cellphone = forms.CharField(
		label='Celular',
        widget=widgets.Phone(attrs={'class': 'form-control form-control-user international_phone'}),
        max_length=15, 
        required=False
    )

    class Meta:
        model = Customer
        fields = [
            'person_type',
            'name',
            'trading_name',
            'cpf',
            'cnpj',
            'tax_regime',
            'tax_payer_type',
            'state_registration',
            'municipal_registration',
            'email',
            'cellphone',
            'phone',
            'notes',
            'credit_limit',
            'is_exempt'
        ]
        
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        person_type = cleaned_data.get('person_type')
        cpf_cnpj_value = None
        if person_type == 'PF':
            if not cleaned_data.get('cpf'):
                raise forms.ValidationError('CPF é obrigatório para pessoa física.')
            cpf_cnpj_value = cleaned_data.get('cpf')
        elif person_type == 'PJ':
            if not cleaned_data.get('cnpj'):
                raise forms.ValidationError('CNPJ é obrigatório para pessoa jurídica.')
            cpf_cnpj_value = cleaned_data.get('cnpj')
        
        if cpf_cnpj_value and self.company:
            if Customer.objects.filter(
                company=self.company,
                cpf_cnpj=cpf_cnpj_value
            ).exists():
                raise forms.ValidationError('Já existe um cliente com este CPF/CNPJ nesta empresa.')
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.partner_type = instance.PARTNER_TYPE.CUSTOMER
    
        if instance.person_type == instance.PERSON_TYPE.PF:
            instance.cpf_cnpj = self.cleaned_data['cpf']
        else:
            instance.cpf_cnpj = self.cleaned_data['cnpj']

        if commit:
            instance.save()
        return instance
