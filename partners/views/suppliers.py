from django.views.generic import TemplateView, ListView
from partners.models.suppliers import Supplier

class SupplierListView(ListView):
    """
        View para listar fornecedores da Empresa.
    """
    model = Supplier
    template_name = 'suppliers/list_view.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.company_active
        context['suppliers'] = company.suppliers.filter(company=company)
        return context


class SupplierTemplateView(TemplateView):
    """
        View para renderizar o template base do cadastro de Fornecedores.
    """
    template_name = 'suppliers/layouts/base.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)