from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from inventory.forms.unit import UnitForm
from inventory.models.units import Unit
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Q


class UnitListView(ListView):
    """
        View para listar unidades de medida.
    """
    model = Unit
    template_name = 'unit/shadcn_list.html'
    partial_template_name = 'unit/partials/unit_table.html'
    paginate_by = 20
    
    def get_queryset(self):
        company = self.request.user.company_active

        queryset = Unit.objects.filter(
            company=company,
            is_active=True
        )
        
        search = self.request.GET.get('search', '')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(abbreviation__icontains=search)
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


class UnitCreateView(CreateView):
    """
        View para criar uma nova unidade de medida.
    """
    model = Unit
    form_class = UnitForm
    template_name = 'unit/shadcn_form.html'
    success_url = reverse_lazy('inventory:unit_list')

    def form_valid(self, form):
        form.instance.company = self.request.user.company_active
        return super().form_valid(form)


class UnitUpdateView(UpdateView):
    """
        View para editar uma unidade de medida existente.
    """
    model = Unit
    form_class = UnitForm
    template_name = 'unit/shadcn_form.html'
    success_url = reverse_lazy('inventory:unit_list')

    def get_queryset(self):
        company = self.request.user.company_active
        return Unit.objects.filter(
            company=company,
            is_active=True
        )


class UnitDeleteView(DeleteView):
    """
        View para deletar uma unidade de medida existente.
    """
    model = Unit
    template_name = 'unit/includes/delete_view.html'
    success_url = reverse_lazy('inventory:unit_list')

    def get_queryset(self):
        company = self.request.user.company_active
        return Unit.objects.filter(
            company=company,
            is_active=True
        )
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.success_url)
