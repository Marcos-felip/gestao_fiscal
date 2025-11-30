from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from inventory.forms.category import CategoryForm
from inventory.models.category import Category
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Q


class CategoryListView(ListView):
    """
        View para listar categorias de produtos.
    """
    model = Category
    template_name = 'category/list_view.html'
    partial_template_name = 'category/includes/list_view.html'
    paginate_by = 20
    
    def get_queryset(self):
        company = self.request.user.company_active
        queryset = Category.objects.filter(
            company=company,
            is_active=True
        )
        
        search = self.request.GET.get('search', '')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
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


class CategoryCreateView(CreateView):
    """
        View para criar uma nova categoria de produto.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'category/create_view.html'
    success_url = reverse_lazy('inventory:category_list')

    def form_valid(self, form):
        form.instance.company = self.request.user.company_active
        return super().form_valid(form)
    

class CategoryUpdateView(UpdateView):
    """
        View para editar uma categoria de produto existente.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'category/create_view.html'
    success_url = reverse_lazy('inventory:category_list')

    def get_queryset(self):
        company = self.request.user.company_active
        return Category.objects.filter(
            company=company,
            is_active=True
        )


class CategoryDeleteView(DeleteView):
    """
        View para deleter uma categoria de produto.
    """
    model = Category
    template_name = 'category/includes/delete_view.html'
    success_url = reverse_lazy('inventory:category_list')

    def get_queryset(self):
        company = self.request.user.company_active
        return Category.objects.filter(
            company=company,
            is_active=True
        )
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # TODO: implementar verificação para nao deletar uma categoria com produtos associados
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.success_url)
