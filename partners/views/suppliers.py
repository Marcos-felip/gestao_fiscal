from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from partners.forms.suppliers import SupplierAddressForm, SupplierAdvancedForm, SupplierBasicForm
from partners.models.suppliers import Supplier
from django.urls import reverse_lazy


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


class SupplierBasicCreateView(CreateView):
    """
        View para criar um novo fornecedor básico.
    """
    model = Supplier
    form_class = SupplierBasicForm
    template_name = 'suppliers/forms/basic_info.html'

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
    template_name = 'suppliers/forms/basic_info.html'
    success_url = reverse_lazy('partners:supplier_list')

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
    template_name = 'suppliers/forms/advanced_info.html'
    success_url = reverse_lazy('partners:supplier_list')

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
    template_name = 'suppliers/forms/address.html'
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