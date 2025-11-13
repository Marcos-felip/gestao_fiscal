from django.views.generic import TemplateView, ListView, CreateView
from partners.models.customers import Customer
from partners.forms.customers import CustomerBasicForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_form'] = CustomerBasicForm()
        return context
    

class CustomerBasicCreateView(CreateView):
    """
        View para criar um novo cliente básico.
    """
    model = Customer
    form_class = CustomerBasicForm
    template_name = 'customers/forms/basic_info.html'
    success_url = reverse_lazy('partners:customer_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        return kwargs

    def form_valid(self, form):
        form.instance.company = self.request.user.company_active
        return super().form_valid(form)
