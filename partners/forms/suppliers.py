from django import forms
from partners.models.suppliers import Supplier
from core.models.address import Address
from core import widgets

class SupplierBasicForm(forms.ModelForm):
    """Formulário com informações essenciais para criação do fornecedor"""
    cpf = forms.CharField(max_length=14, label='CPF', required=False)
    cnpj = forms.CharField(max_length=18, label='CNPJ', required=False)
    email = forms.EmailField(required=True)
    cellphone = forms.CharField(
        label='Celular',
        widget=widgets.Phone(attrs={'class': 'form-control form-control-user international_phone'}),
        max_length=15, 
        required=False
    )

    class Meta:
        model = Supplier
        fields = [
            'person_type',
            'name',
            'trading_name',
            'cpf',
            'cnpj',
            'email',
            'cellphone',
            'phone',
        ]
        
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.cpf_cnpj:
            if self.instance.person_type == 'PF':
                self.initial['cpf'] = self.instance.cpf_cnpj
            else:
                self.initial['cnpj'] = self.instance.cpf_cnpj

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = ''.join(filter(str.isdigit, cpf))
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve conter 11 dígitos.')
        return cpf

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            cnpj = ''.join(filter(str.isdigit, cnpj))
            if len(cnpj) != 14:
                raise forms.ValidationError('CNPJ deve conter 14 dígitos.')
        return cnpj

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
            existing_suppliers = Supplier.objects.filter(
                company=self.company,
                cpf_cnpj=cpf_cnpj_value
            )
            
            if self.instance and self.instance.pk:
                existing_suppliers = existing_suppliers.exclude(pk=self.instance.pk)
            
            if existing_suppliers.exists():
                raise forms.ValidationError('Já existe um fornecedor com este CPF/CNPJ nesta empresa.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.partner_type = instance.PARTNER_TYPE.SUPPLIER
    
        if instance.person_type == instance.PERSON_TYPE.PF:
            instance.cpf_cnpj = self.cleaned_data['cpf']
        else:
            instance.cpf_cnpj = self.cleaned_data['cnpj']

        if commit:
            instance.save()
        return instance


class SupplierAdvancedForm(forms.ModelForm):
    """Formulário com informações fiscais e comerciais avançadas"""
    
    class Meta:
        model = Supplier
        fields = [
            'tax_regime',
            'tax_payer_type',
            'state_registration',
            'municipal_registration',
            'credit_limit',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control form-control-user',
                'rows': 4,
                'placeholder': 'Observações sobre o cliente...'
            }),
            'credit_limit': forms.NumberInput(attrs={
                'class': 'form-control form-control-user',
                'placeholder': '0,00'
            }),
            'state_registration': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Inscrição Estadual'
            }),
            'municipal_registration': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Inscrição Municipal'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.person_type == 'PF':
            self.fields['tax_regime'].required = False
            self.fields['state_registration'].required = False
            self.fields['municipal_registration'].required = False


    def clean_state_registration(self):
        state_registration = self.cleaned_data.get('state_registration')
        if state_registration:
            state_registration = ''.join(filter(str.isalnum, state_registration))
        return state_registration

    def clean_credit_limit(self):
        credit_limit = self.cleaned_data.get('credit_limit')
        if credit_limit and credit_limit < 0:
            raise forms.ValidationError('O limite de crédito não pode ser negativo.')
        return credit_limit


class SupplierAddressForm(forms.ModelForm):
    postal_code = forms.CharField(
        max_length=9,
        label='CEP',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': '00000-000',
        }),
        required=True
    )
    
    street = forms.CharField(
        max_length=255,
        label='Logradouro',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Rua, Avenida, etc.'
        }),
        required=True
    )
    
    number = forms.CharField(
        max_length=20,
        label='Número',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Número'
        }),
        required=False
    )
    
    complement = forms.CharField(
        max_length=60,
        label='Complemento',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Apto, Bloco, etc.'
        }),
        required=False
    )
    
    district = forms.CharField(
        max_length=80,
        label='Bairro',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
        }),
        required=True
    )
    
    city_name = forms.CharField(
        max_length=120,
        label='Cidade',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
        }),
        required=True
    )
    
    state = forms.CharField(
        max_length=2,
        label='Estado',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'SP, RJ, etc.'
        }),
        required=True
    )
    
    city_ibge_code = forms.CharField(
        max_length=7,
        label='Código IBGE',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Código IBGE da cidade'
        }),
        required=False,
        help_text='Código IBGE da cidade (7 dígitos)'
    )

    class Meta:
        model = Address
        fields = [
            'postal_code',
            'street',
            'number',
            'complement',
            'district',
            'city_name',
            'state',
            'city_ibge_code'
        ]

    def __init__(self, *args, **kwargs):
        self.supplier = kwargs.pop('supplier', None)
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if postal_code:
            postal_code = ''.join(filter(str.isdigit, postal_code))
            if len(postal_code) != 8:
                raise forms.ValidationError('CEP deve conter 8 dígitos.')
        return postal_code

    def clean_city_ibge_code(self):
        city_ibge_code = self.cleaned_data.get('city_ibge_code')
        if city_ibge_code:
            city_ibge_code = ''.join(filter(str.isdigit, city_ibge_code))
            if len(city_ibge_code) != 7:
                raise forms.ValidationError('Código IBGE deve conter 7 dígitos.')
        return city_ibge_code

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if state:
            state = state.upper()
            valid_states = [
                'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
                'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
                'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
            ]
            if state not in valid_states:
                raise forms.ValidationError('Estado inválido. Use a sigla do estado (ex: SP, RJ).')
        return state

    def save(self, commit=True):
        address = super().save(commit=True)
        
        if self.supplier and not self.supplier.address:
            self.supplier.address = address
            self.supplier.save()
            
        return address
