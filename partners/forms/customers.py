from django import forms
from partners.models.customers import Customer


class CustomerBasicForm(forms.ModelForm):
	cpf = forms.CharField(max_length=11, label='CPF', required=True)
	cnpj = forms.CharField(max_length=14, label='CNPJ', required=True)
	address = forms.CharField(widget=forms.Textarea, label='Endereço', required=False)

	class Meta:
		model = Customer
		fields = [
			'name',
			'trading_name',
			'person_type',
			'cpf',
			'cnpj',
			'tax_regime',
			'tax_payer_type',
			'state_registration',
			'municipal_registration',
			'email',
			'phone',
			'cellphone',
			'address',
			'notes',
			'credit_limit',
			'is_exempt'
		]

	def save(self, commit=True):
		instance = super().save(commit=False)
		instance.partner_type = instance.PARTNER_TYPE.CUSTOMER
		if commit:
			instance.save()
			self.save_m2m()
		return instance
