from django.views.generic import TemplateView, ListView, CreateView
from partners.forms.customers import CustomerForm
from partners.models.customers import Customer
from django.urls import reverse_lazy


class CustomerListView(ListView):
    """
        View para listar clientes da Empresa.
    """
    model = Customer
    template_name = 'customers/list_view.html'
    paginate_by = 20

    def get_queryset(self):
        company = self.request.user.company_active
        queryset = Customer.objects.filter(company=company)
        return queryset


class CustomerTemplateView(TemplateView):
    """
        View para renderizar o template base do cadastro de clientes.
    """
    template_name = 'customers/layouts/base.html'