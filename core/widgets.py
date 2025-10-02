from django import forms


class Phone(forms.TextInput):
    template_name = 'custom_widgets/phone.html'
    
    def __init__(self, attrs=None):
        if not attrs:
            attrs = {}
        attrs['class'] = 'international_phone'
        attrs['inputmode'] = 'tel'
        super(Phone, self).__init__(attrs)

    class Media:
        js = ["js/phone.js"]