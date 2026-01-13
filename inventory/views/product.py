from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from inventory.models.product import Product, ProductFiscalData
from inventory.forms.product import ProductDataForm, ProductTaxForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect


class ProductListView(ListView):
    """
        View para listar produtos da Empresa.
    """
    model = Product
    template_name = 'product/list_view.html'
    partial_template_name = 'product/partials/product_table.html'
    paginate_by = 20

    def get_queryset(self):
        company = self.request.user.company_active
        queryset = Product.objects.filter(company=company, is_active=True)

        # Aplicar filtros
        search = self.request.GET.get('search', '')
        
        # Busca por nome, SKU ou código de barras
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(sku__icontains=search) |
                Q(barcode__icontains=search)
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


class ProductTemplateView(TemplateView):
    """
        View para renderizar o template base do produto.
    """
    template_name = 'product/layouts/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_form'] = ProductDataForm()
        return context
    

class ProductDataCreateView(CreateView):
    """
        View para criar um novo produto.
    """
    model = Product
    form_class = ProductDataForm
    template_name = 'product/create_view_data_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'data'
        return context

    def get_success_url(self):
        return reverse_lazy('inventory:product_tax', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        return kwargs

    def form_valid(self, form):
        form.instance.company = self.request.user.company_active
        return super().form_valid(form)


class ProductDataUpdateView(UpdateView):
    """
        View para atualizar um produto.
    """
    model = Product
    form_class = ProductDataForm
    template_name = 'product/create_view_data_form.html'
    success_url = reverse_lazy('inventory:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'data'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        return kwargs


class ProductTaxUpdateView(UpdateView):
    """
        View para atualizar dados fiscais de um produto.
    """
    model = Product
    form_class = ProductTaxForm
    template_name = 'product/create_view_tax_form.html'

    def get_success_url(self):
        return reverse_lazy('inventory:product_tax', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        self.product = product
        if not product.fiscal_data:
            product.fiscal_data = ProductFiscalData.objects.create(company=product.company)
            product.save()
        return product.fiscal_data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company_active
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.product
        context['active_tab'] = 'tax'
        return context


class ProductDeleteView(DeleteView):
    """
        View para deletar um produto.
    """
    model = Product
    template_name = 'product/includes/delete_view.html'
    success_url = reverse_lazy('inventory:product_list')

    def get_queryset(self):
        company = self.request.user.company_active
        return Product.objects.filter(company=company, is_active=True)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.success_url)