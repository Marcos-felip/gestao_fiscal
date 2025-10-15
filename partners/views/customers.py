from django.views.generic import ListView
from partners.models.customers import Customer


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

