from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from partners.models.customers import Customer
from core.models.address import Address
from partners.forms.customers import CustomerAddressForm, CustomerAdvancedForm, CustomerBasicForm
from django.urls import reverse_lazy
from django.db.models import Q


class CustomerListView(ListView):
    """
        View para listar clientes da Empresa.
    """
    model = Customer
    template_name = 'customers/list_view.html'
    partial_template_name = 'customers/includes/list_view.html'
    paginate_by = 20

    def get_queryset(self):
        company = self.request.user.company_active
        queryset = Customer.objects.filter(company=company)

        # Aplicar filtros
        search = self.request.GET.get('search', '')
        
        # Busca por nome, nome fantasia ou CPF/CNPJ
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(trading_name__icontains=search) |
                Q(cpf_cnpj__icontains=search)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_search'] = self.request.GET.get('search', '')
        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('Hx-Request'):
            self.template_name = self.partial_template_name
        return super().render_to_response(context, **response_kwargs)


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

    def get_success_url(self):
        return reverse_lazy('partners:customer_advanced', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        return kwargs

    def form_valid(self, form):
        form.instance.company = self.request.user.company_active
        return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    """
        View para atualizar um cliente existente.
    """
    model = Customer
    form_class = CustomerBasicForm
    template_name = 'customers/forms/basic_info.html'
    success_url = reverse_lazy('partners:customer_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        return kwargs


class CustomerAdvancedUpdateView(UpdateView):
    """
        View para atualizar informações avançadas de um cliente existente.
    """
    model = Customer
    form_class = CustomerAdvancedForm
    template_name = 'customers/forms/advanced_info.html'

    def get_success_url(self):
        return reverse_lazy('partners:customer_advanced', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        return kwargs


class CustomerAddressUpdateView(UpdateView):
    """
        View para atualizar o endereço de um cliente existente.
    """
    model = Customer
    form_class = CustomerAddressForm
    template_name = 'customers/forms/address.html'

    def get_success_url(self):
        return reverse_lazy('partners:customer_address', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        customer = super().get_object(queryset)
        self.customer = customer
        return customer

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        kwargs['customer'] = self.customer
        
        if self.customer.address:
            kwargs['instance'] = self.customer.address
        else:
            kwargs.pop('instance', None)
        
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.customer
        return context
