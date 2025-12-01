from django import forms
from inventory.models.units import Unit


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'name',
            'abbreviation'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'abbreviation': forms.TextInput(attrs={'class': 'form-control'}),
        }