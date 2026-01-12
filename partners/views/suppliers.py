from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from partners.forms.suppliers import SupplierAddressForm, SupplierAdvancedForm, SupplierBasicForm
from partners.models.suppliers import Supplier
from django.urls import reverse_lazy
from django.db.models import Q


class SupplierListView(ListView):
    """
        View para listar fornecedores da Empresa.
    """
    model = Supplier
    template_name = 'suppliers/shadcn_list.html'
    partial_template_name = 'suppliers/partials/supplier_table.html'
    paginate_by = 20

    def get_queryset(self):
        company = self.request.user.company_active
        queryset = Supplier.objects.filter(company=company)

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


class SupplierTemplateView(TemplateView):
    """
        View para renderizar o template base do cadastro de Fornecedores.
    """
    template_name = 'suppliers/layouts/base.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class SupplierBasicCreateView(CreateView):
    """
        View para criar um novo fornecedor básico.
    """
    model = Supplier
    form_class = SupplierBasicForm
    template_name = 'suppliers/shadcn_basic_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'basic'
        return context

    def get_success_url(self):
        return reverse_lazy('partners:supplier_advanced', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        return kwargs

    def form_valid(self, form):
        form.instance.company = self.request.user.company_active
        return super().form_valid(form)
    

class SupplierUpdateView(UpdateView):
    """
        View para atualizar um fornecedor existente.
    """
    model = Supplier
    form_class = SupplierBasicForm
    template_name = 'suppliers/shadcn_basic_form.html'
    success_url = reverse_lazy('partners:supplier_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'basic'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        return kwargs


class SupplierAdvancedUpdateView(UpdateView):
    """
        View para atualizar informações avançadas de um fornecedor existente.
    """
    model = Supplier
    form_class = SupplierAdvancedForm
    template_name = 'suppliers/shadcn_advanced_form.html'
    success_url = reverse_lazy('partners:supplier_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'advanced'
        return context

    def get_success_url(self):
        return reverse_lazy('partners:supplier_advanced', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        return kwargs


class SupplierAddressUpdateView(UpdateView):
    """
        View para atualizar o endereço de um fornecedor existente.
    """
    model = Supplier
    form_class = SupplierAddressForm
    template_name = 'suppliers/shadcn_address_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'address'
        context['object'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy('partners:supplier_address', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        supplier = super().get_object(queryset)
        self.supplier = supplier
        return supplier

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        kwargs['supplier'] = self.supplier
        
        if self.supplier.address:
            kwargs['instance'] = self.supplier.address
        else:
            kwargs.pop('instance', None)
        
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.supplier
        return context