from django.urls import reverse_lazy
from django.views.generic import UpdateView
from accounts.models.company import Company
from configuration.forms.company import CompanyForm


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/create_view.html'

    def success_url(self):
        return reverse_lazy('configuration:company_update', kwargs={'pk': self.get_object().pk})

    def get_object(self, queryset=None):
        return self.request.user.company_active

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.get_object()
        return kwargs
